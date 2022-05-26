

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

s.bind(("0.0.0.0", 50000))
s.listen(1)

try:
    while True:
        conn, addr = s.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                conn.close()
                break

            print(addr, len(data))
finally:
    s.close()
