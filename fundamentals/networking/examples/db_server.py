import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.settimeout(0.2)
server.bind(("", 13337))

message = b"your very important message"

while True:
    server.sendto(message, ('192.168.0.255', 58866))
    print("message sent!")
    time.sleep(1)