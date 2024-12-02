#!/usr/bin/env python3

import socket

from jwt import DecodeError

MPORT = 5007
MGROUP = '224.1.1.1'
IFADDR = '0.0.0.0'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.bind((MGROUP, MPORT))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MGROUP) + socket.inet_aton(IFADDR))

    print('Waiting for data...')
    while True:
        received = sock.recv(1500)
        try:
            print(f'Received packet: {received.decode()}')
        except UnicodeDecodeError:
            hex_data = received.hex().upper()
            print(f'Received packet: {" ".join(hex_data[i:i + 4] for i in range(0, len(hex_data), 4))}')


if __name__ == '__main__':
    main()
