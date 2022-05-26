import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.settimeout(0.2)
server.bind(("", 13338))

message = b"your very important message"

while True:
    server.sendto(message, ('', 58866))
    print("message sent!")
    time.sleep(1)