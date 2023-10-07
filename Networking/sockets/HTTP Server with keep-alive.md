```python
import socket

SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
server_socket.bind((socket.gethostname(), SERVER_PORT))
server_socket.listen()
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    while True:
        # Get the client request
        request = client_connection.recv(1024).decode()
        print(request)
        if not request:
            break

        # The text to serve
        message = "Hello, World!"

        content_length = len(message.encode("utf-8"))

        # Send HTTP response
        response = f'HTTP/1.1 200 OK\nContent-Length: {content_length}\n\n{message}'
        client_connection.send(response.encode())

    client_connection.close()

# Close socket
server_socket.close()

```

