#!/usr/bin/python
import socket
import struct
import time

# Create an UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Let multiple processes use the same port
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('',MULTICAST_PORT))


mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_ADDRESS), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # sending IGMPv2 membership queries
print("Joined Multicast-Address: " + MULTICAST_ADDRESS + " ... listening on udp port " + str(MULTICAST_PORT))
while True:
	print sock.recv(10240)
	time.sleep(0.02)