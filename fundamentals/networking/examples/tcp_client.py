import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(('127.0.0.2', 50000))
try: 
    while True: 
        s.send(b'Hello!')
finally: 
    s.close()