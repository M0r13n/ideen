import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(('', 50001))

# This send s a IGMP message to announce that this machine joined the 224.1.1.1 group
s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton('224.0.0.50') + socket.inet_aton('192.168.0.53'))

while True:
    data, addr = s.recvfrom(1024)
    print(data, addr)