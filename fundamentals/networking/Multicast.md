# Multicast Overview

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

## Loop prevention

## Addressing

## Layer 2 

## IGMP


Refer to: https://www.juniper.net/documentation/us/en/software/junos/multicast/topics/concept/multicast-ip-overview.html