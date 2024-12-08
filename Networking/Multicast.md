## Use cases

- send datagrams to a set of hosts that can be on different subnetworks
- hosts can join and leave multicast groups to receive or stop receiving multicast datagrams
- as for all IP datagrams multicast uses **best effort delivery** ([[IPv4]])
- no restrictions on the physical location or the number of members in a multicast group
- a host can be a member **of more than one multicast group at any time**
- a host **does not have to belong to a group to send packets** to members of a group
- routers use the **IGMP (Internet Group Membership Protocol)** to learn about the presence of group members
- **one-to-many delivery**
- transmitting host generates only a single stream of IP packets, so the load remains constant whether there is one receiver or one million
- network routing devices replicate the packets and deliver the packets to the proper receivers
- links leading to subnets consisting of entirely uninterested receivers carry no multicast traffic
==-> reduces the burden placed on sender, network and receiver==

## Challenges

- routing devices must find multicast sources on the network
- routing devices  must send out copies of packets on several interfaces
- prevent loops
- connect interested destinations with the proper source
- reduce the flow of unwanted packets to a minimum

## Addressing

- formerly known as [[IPv4#Class D| Class D]] network
- addresses range from `224.0.0.0` through `239.255.255.255`
- which is `1110 0000` through `1110 1111`
-  first 4 bits set for network -> every IP starting with `1110` is a multicast IP
- 28 bits for hosts -> number of multicast groups
- typically Multicast addresses have a `/32` prefix -> all bits set
- **relate to content, not to physical devices.**
	- every device has it's own Unicast IP
	- Multicast addresses **can never** be source addresses
- special ranges:
	- 224.0.0.1 through 224.0.0.255 is used for local wire usage
	- 239.0.0.0 through 239.255.255.255 is reserved for administratively scoped addresses
- *Which destination MAC address for the frame corresponds to the packet’s multicast group address?*
	- use the MAC range `0x01-00-5E-00-00-00` to `0x01-00-5E-FF-FF-FF`
	- `00-00-00` to `FF-FF-FF` leaves `4x6=24` bits available for addressing
	- this is less than the `28` bits of Multicast host addresses
	- -> it is deliberately tolerated that multiple IP addresses map to the same MAC
	- [How to convert an IP to a MAC](https://www.juniper.net/documentation/us/en/software/junos/multicast/topics/concept/multicast-ip-overview.html#multicast-overview__id-g016859)


### Frame distribution

- **Layer1**: Forward to all HUB users
- **Layer 2(dump)**: Send out frames as broadcast
- **Layer 2(multicast)**: Learning of group members, specific forwarding

To avoid multicast routing loops, every multicast routing device must always be aware of the interface that leads to the source of that multicast group content by the shortest path. This is the upstream (incoming) interface, and packets are never to be forwarded back toward a multicast source. All other interfaces are potential downstream (outgoing) interfaces, depending on the number of branches on the distribution tree.


## Loop prevention

Refer to: https://www.juniper.net/documentation/us/en/software/junos/multicast/topics/concept/multicast-ip-overview.html

## Multicast with many interfaces

- an application has to join a multicast group **on every interface** in order to receive multicast packets
- when listening: if no interface is explicitly chosen, **then the Kernel chooses an interface** (typically the default interface)
- when sending: if not interface is explicitly chosen, then the first interface that **matches the routing table** is chosen
- `igmpproxy` might be helpful to route Multicast traffic between interfaces
  - **Linux does NOT route multicast**
- do not forget about `ip maddr show`

### Examples

#### Listen and let the Kernel decide

- bind to all interfaces
- listen to `0.0.0.0`
- the Kernel will choose an interface and an IP for the application
- use `sudo ip route add 224.0.0.0/4 via 10.0.0.1` (or similar) to influence the Kernels behavior
  - the Kernel will chose a matching source IP based on the route

```python
#!/usr/bin/env python3

import socket


MPORT = 5007
MGROUP = '224.1.1.1'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # INADDR_ANY
    sock.bind(('', MPORT))

    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MGROUP) + socket.inet_aton('0.0.0.0'))

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
```

#### Send to a specific interface

Usually, the system administrator specifies the default interface multicast datagrams should be sent from. The programmer can override this and choose a concrete outgoing interface for a given socket with this option ([`IP_MULTICAST_IF.`](https://tldp.org/HOWTO/Multicast-HOWTO-6.html#ss6.4)).

```C
struct in_addr interface_addr;
setsockopt (socket, IPPROTO_IP, IP_MULTICAST_IF, &interface_addr, sizeof(interface_addr));
```

From now on, all multicast traffic generated in this socket will be output from the interface chosen. To revert to the original behavior and let the kernel choose the outgoing interface based on the system administrator's configuration, it is enough to call `setsockopt()` with this same option and INADDR_ANY in the interface field.

```py
import random
import socket
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MULTICAST_TTL = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

# This line decides which interface to use.
# This line can be omitted. Then the Kernel chooses the interface for the application.
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton('127.0.0.1'))

while True:
    print('Sending')
    sock.sendto(random.randbytes(12), (MCAST_GRP, MCAST_PORT))
    time.sleep(1)
```

#### Listen on all interfaces

- bind to `INADDR_ANY`
- call `setsockopt` with `IP_ADD_MEMBERSHIP` on each interface you want to receive multicast on
- `setsockopt` with `IP_MULTICAST_IF` on the interface you want to send multicast on

```py
#!/usr/bin/env python3

import socket


MPORT = 5007
MGROUP = '224.1.1.2'


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)

    sock.bind(('', MPORT))

    # Do this for each socket
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MGROUP) + socket.inet_aton('127.0.0.1'))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MGROUP) + socket.inet_aton('192.168.64.3'))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MGROUP) + socket.inet_aton('10.0.0.1'))

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
```
