[[DHCPv4|DHCP]] Snooping defends against two kinds of DHCP-based attacks:

- **DHCP spoofing**: an attacker responds with fake DHCP messages in an attempt to hijack IP addresses or to position itself to be the standard gateway/ DNS server (MitM attack)
- **DHCP starvation:** an attacker floods the network with DHCP requests in order to cause the DHCP server to run out of available IP addresses

## How does it work?

Basically, DHCP Snooping is a layer of protection that works on layer 2 on the network switch. It enables the switch to learn MAC/IP addresses in order to detect untrusted DHCP messages. To learn these information switch ports are divided into trusted and untrusted ports. Everything that passes through trusted ports is remembered and stored in a dynamic database inside the switch.

![[dhcp_snooping.png]]

A **"binding anchor"** as defined in [RFC 7039](https://datatracker.ietf.org/doc/html/rfc7039) is an attribute that is immutable or difficult to change that may be used to identify the system an IP address has been assigned to; common examples include a Media Access Control (MAC) address found on an Ethernet switch port or Wi-Fi security association.

For DHCP snooping to function properly, all DHCP servers must be connected to the switch through trusted interfaces, as untrusted DHCP messages will be forwarded only to trusted interface.

Each switch builds and maintains the **DHCP snooping binding table**. This databse contains an entry for each untrusted host with a leased IP address. Hosts connected to trusted ports are not tracked in this database. The database is updated when the switch receives specific DHCP messages such as DHCPACK or DHCPRELEASE.

Packets are dropped in any of the following conditions occur:

1. the switch receives a DHCP message originating from a DHCP server outside the network
2. the switch receives a packet on an untrusted interface, and the source MAC address and the DHCP  client hardware address do not match
3. the switch receives a DHCPRELEASE message from an untrusted host with  an entry in the DHCP snooping binding table, and the interface information in the binding table does  not match the interface on which the message was received

## Mikrotik Configuration

Enable the DHCP snooping feature:
`/interface/bridge/ set dhcp-snooping=yes`

Mark a port as trusted:
`/interface/bridge/port/ set trusted=yes`