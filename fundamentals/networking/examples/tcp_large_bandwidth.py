import socket
import time
import itertools

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(('192.168.0.53', 50000))

unlimited_bytes = itertools.repeat(b'X' * 1024)

try: 
    for chunk in unlimited_bytes: 
        s.send(chunk)
finally: 
    s.close()