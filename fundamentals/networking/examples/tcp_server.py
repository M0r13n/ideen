

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("0.0.0.0", 50000))
s.listen(1)


total = 0
start = time.time()
last_print = start

GB = 1000000000

try:
    while True:
        conn, addr = s.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                conn.close()
                break

            total += len(data)

            now = time.time()
            if now > last_print + 1:
                tot_time = now - last_print
                last_print = now
                print('Recv rate:', round(((total / tot_time) / GB)*8, 3), 'Gbits/s')
                total = 0
finally:
    s.close()
