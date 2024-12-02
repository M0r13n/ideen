#!/usr/bin/env python3

import socket

MPORT = 5007
MGROUP = '224.1.1.1'
IFADDR = '192.168.64.3'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.bind((MGROUP, MPORT))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MGROUP) + socket.inet_aton(IFADDR))

    print('Waiting for data...')
    while True:
        received = sock.recv(1500)
        print('Received packet of {0} bytes'.format(len(received)))


if __name__ == '__main__':
    main()
