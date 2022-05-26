import socket
import time

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('127.0.0.1', 50000))
    try: 
        s.send(b'Hello!')
    finally: 
        s.close()
    
    time.sleep(1)