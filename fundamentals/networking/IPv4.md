# IPv4

- Layer 3 or Network Layer protocol
- used for host-to-host communication
- serves two basic functions:
	- **addressing**: transmit datagrams to specific destinations
	- **fragmentation**: fragment and reassemble *large* datagrams  for transmission through *small packet* networks
* **connectionless**
	-> ==each packet is treated differently==
	-> sessionless (unlike TCP)
	-> each datagram may take a different path
* **best effort delivery**: No guarantee of packet delivery
	-> this has to be done in layers above (e.g. TCP in the transport layer)
* **unreliable**
	-> datagrams may get dropped
	-> datagrams may be delivered out of order
	-> datagrams may be duplicated 
	-> ==no error control for data, only a header checksum==

## IP Addressing

### What is an IP address?
* used to ==identify== specific devices on a network
	* like street, number and city point to specific house in a city
* **globally unique** for every device on the internet
	* there are exceptions:
		* [[1918|RFC1918]]
		* loopback and broadcast addresses
* 32 bits -> 2 pow 32 address -> 4294967296 possible addresses
* four octets: 123.123.123.123
* **Network Address Portion**
	* identifies a specific network
	* ==routers use networks route packets==: routers do NOT route single IPs
* **Host Address Portion
	* identifies a specific device **on a network**

#### Class based networks

The following network "classes" are superseded by [[CIDR]].

###### Class A
- /8 network -> first 8 bits set for network 
- range from 1 to 126 (`0000 0000` to `0111 1111`) (0 and 127 reserved)

###### Class B
* /16 network -> first 16 bits set for network
* range from 128 to 191 (`1000 0000` to `1011 1111`)

###### Class C
- /24 network -> first 24 bits set for network
- range from 192 to 223 (`1100 0000` to `1101 1111`)

### Directed Broadcast Address
- send data to **all** devices on a network
- entire host portion is 1s -> 192.168.1.0/24 implies 192.168.1.255 as a directed broadcast address
- not routed by default

### Local Broadcast Address
- send data to **all** devices on the **local** network
- all binary 1s -> `11111111.11111111.11111111.11111111` -> `255.255.255.255`
- used by DHCP to assign IP addresses to device that initially do not know anything about the network
- always dropped by Layer 3 devices

### Loopback Addresses
- all addresses starting with 127
- most famous: 127.0.0.1
- fun fact: because this is a /8 network 16 millions addresses are wasted

### Link local Addresses
- described by [RFC 3927](https://datatracker.ietf.org/doc/html/rfc3927)
- network 169.254.0.0/16
- allows the communication between devices if no DHCP server is available
- host portion is randomly chosen
- ==allows for immediate communication of two devices if connected directly==
- no manual configuration is required
- **NOT routable**: only valid on the local link (broadcast domain)


## IP Header

```txt
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
