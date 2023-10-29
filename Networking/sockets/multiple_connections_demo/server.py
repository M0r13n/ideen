import select
import socket
import threading

SERVER_PORT = 8000
MAX_CLIENTS_PER_THREAD = 2
MAX_NUM_THREADS = 5

# List of all active threads
threads: list['SocketHandlerThread'] = []
threads_lock = threading.Lock()


class SocketHandlerThread(threading.Thread):
    # Simple thread than handles multiple connections (sockets).
    # Active connections are tracked in a list and are removed when closed.
    # Uses select.select() to poll ready sockets without blocking.

    def __init__(self, client_connection):
        threading.Thread.__init__(self)
        self.clients = [client_connection, ]
        self.c_lock = threading.Lock()

    def run(self):
        # Continuously poll for sockets ready for reading.
        while True:
            with self.c_lock:
                clients = self.clients
            if not clients:
                break
            ready, _, _ = select.select(clients, [], [])
            for client in ready:
                self.handle_client(client)

        # Remove the thread from the list of active tracks, once it has no connections to track
        with threads_lock:
            print('No more connections. Closing thread..')
            threads.remove(self)

    def add_client(self, client):
        if not self.has_capacity():
            raise ValueError('can not fit any more clients')
        with self.c_lock:
            self.clients.append(client)

    def del_client(self, client):
        with self.c_lock:
            self.clients.remove(client)

    def has_capacity(self):
        with self.c_lock:
            return len(self.clients) < MAX_CLIENTS_PER_THREAD

    def handle_client(self, client_connection):
        # Get the client request
        request = client_connection.recv(1024).decode()
        if not request:
            print('no data. closing')
            client_connection.close()
            self.del_client(client_connection)
            return None

        # The text to serve
        message = "Hello, World!"

        # Send HTTP response
        content_length = len(message.encode("utf-8"))
        response = f'HTTP/1.1 200 OK\nContent-Length: {content_length}\n\n{message}'
        client_connection.send(response.encode())
        return None


if __name__ == '__main__':
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server_socket.bind((socket.gethostname(), SERVER_PORT))
    server_socket.listen()
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        # Wait for client connections
        c_conn, client_addr = server_socket.accept()

        for thread in threads:
            if thread.has_capacity():
                print('Found thread with capacity.')
                thread.add_client(c_conn)
                break
        else:
            print('Creating new thread.')
            t_thread = SocketHandlerThread(c_conn)
            with threads_lock:
                threads.append(t_thread)
            t_thread.start()

    # Close socket
    server_socket.close()
