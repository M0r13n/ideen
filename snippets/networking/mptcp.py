import socket
import sys

# Only on Python 3.10 and above, socket.IPPROTO_MPTCP is defined.
try:
    IPPROTO_MPTCP = socket.IPPROTO_MPTCP
except AttributeError:
    IPPROTO_MPTCP = 262


def create_socket(sockaf):
    try:
        sock = socket.socket(sockaf, socket.SOCK_STREAM, IPPROTO_MPTCP)
        # dual stack IPv4/IPv6
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return sock
    except OSError as e:
        print(f'ERROR: {e}. MPTCP not supported')
        sys.exit(1)


def http_get(sock, host):
    # craft a very simple HTTP GET request
    request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: curl/8.5.0\r\n"
        f"Accept: */*\r\n"
        f"Connection: close\r\n\r\n"
    )

    sock.sendall(request.encode('utf-8'))

    # Receive reponse
    response = b""
    while True:
        data = sock.recv(4096)
        if not data:
            break
        response += data
    return response


#
# Main
#
host, port = "test.multipath-tcp.org", 80
s = create_socket(socket.AF_INET6)
s.connect((host, port))

# perform a HTTP request
response = http_get(s, host)

# Should result in: You are using MPTCP.
print(response.decode())

s.close()
