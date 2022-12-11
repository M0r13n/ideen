# IPv6

## Dual Stack

Modern operating systems support that a host has an IPv4 and IPv6 address simultaneously. This is used to make the transition from IPv4 to IPv6 easier, because services can be migrated one after another. The only downside is the added complexity. Some things need to be configured twice (routing, firewalls, etc.).

### Address Selection

- a host has both: a global IPv4 and a global IPv6 address
- the host chooses the type of connection for **each new outgoing connection**
- RFC6723 says that IPv6 is preferred over IPv4
- sometimes hosts deviate from this and prefer the faster connection

## IPv4 vs IPv6

|   Difference   |            IPv4            |              IPv6               |
| :------------: | :------------------------: | :-----------------------------: |
|   Bit length   |          32 bits           |            128 bits             |
|    Checksum    | header field for checksums |               no                |
| Fragmentation  |  possible a long the path  |     done only by the sender     |
| Address types  | Uni-,broad- and multicast  |     uni-,multi- and anycast     |
| Configuration  |           DHCPv4           | Auto configuration capabilities |
|  Network MAsk  |            yes             |       uses prefix instead       |
| MAC resolution |            ARP             |  Multicast Neighbor Discovery   |

### How does IPv6 auto configuration work?

IPv6 uses SLAAC (Stateless Address Autoconfiguration) for stateless configuration of IPv6 addresses on a given interface. It is possible to retrieve a link locale and a global IPv6 address. 

- all link locale addresses start with the prefix `fe80:0000:0000:0000/64`
- the suffix (interface identifier) is the EUI-64 identifier
  - split the host MAC address in the middle
  - invert the second bit of the first octet
  - insert the two bytes `ff:fe` between the two halfes
  - `00:0C:F1:8E:C1:D8` -> `00:0C:F1` and `8E:C1:D8`
  - invert second bit `00` -> `02`
  - insert `ff:fe` -> `02:0C:F1:FF:FE:8E:C1:D8`
  - the final address is then: 
    - `fe80:0000:0000:0000:020C:F1FF:FE8E:C1D8`
- before actually using this address a Duplicate Address Detection is required
  - Neighbor Solicitation: Does anyone use this address (Multicast)
  - Neighbor Advertisement: If someone answers, this address is used
- after the host has a link locale address, it can request a global address:
  - Router Solicitation: Ask `ff02::2` for a global prefix
  - Router Advertisement: The next router answers with the global prefix and the MTU
  - the router also sets the **autonomous** flag
- because the MAC address is globally unique, this allows for tracking. Therefore privacy extensions are used to obfuscate the MAC address

### Why does IPv6 does not have header fields for checksums and fragmentation?

Speed. IPv6 was designed to be more efficient than IPv4. Therefore, several decisions were made to speed up the processing of IP packets. Thus, the IP header was greatly simplified and is **fixed length** (unlike in IPv4). Also it is not possible to fragment IPv6 packets along the path, as it can be done with IPv4. This is also the reason why Path MTU Discovery is so important in IPv6.

The checksum was removed in IPv6 because it is mostly redundant. All link layer protocols (Ethernet) provide a checksum. So only the payload itself may contain logic errors. But almost all transport protocols like TCP/UDP have error checking to catch logic errors. Most of these checksums do cover most of the IP header as well (pseudo header).

## Firewall Gotchas

IPv6 uses ICMPv6 for the address resolution. ICMPv6 is based on the IPv6 protocol itself. Therefore, these packets can not be filtered by the firewall. Refer to RFC4890 for Firewall Recommendations.

## IPv6 Addressing

IPv6 support three types of addresses:

- **Unicast**: identify a single interface
- **Anycast**: indentify a set of interfaces in such a way that a packet sent to an anycast address is delivered to a member of the set
- **Multicast**: indentify a group of interfaces in such a way that a packet sent to a multicast address is delivered to all interfaces in the group

| Prefix    | Comment                                  | Example/IPv4 Equivalent      |
| --------- | ---------------------------------------- | ---------------------------- |
| ::/128    | unspecified bind address                 | 0.0.0.0                      |
| ::1/128   | loopback interface                       | 127.0.0.1                    |
| ::ffff/96 | IPv4 mapped                              | ::ffff:192.0.2.1             |
| fc00::/7  | Unique local address (RFC 4193)          | RFC1918 address (10.0.0.0/8) |
| fe80::/10 | Link local Address (54 bits are often 0) | 169.254.0.0/16               |

