- [[Multicast#Use cases|Use cases]]
- [[Multicast#Loop prevention|Loop prevention]]
- [[Multicast#Addressing|Addressing]]
- [[Multicast#Layer 2|Layer 2]]
- [[Multicast#IGMP|IGMP]]

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
	- every device it's own Unicast IP
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