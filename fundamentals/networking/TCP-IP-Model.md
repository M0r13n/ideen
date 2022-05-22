# CISCO TCP/IP model
| TCP/IP Layer | Example(s)|
| --- | --- |
| Application | HTTP, FTP, DHCP, Telnet, TLS|
| Transport | TCP, UDP |
| Network | IPv4, IPv6|
| Data Link | Ethernet |
| Physical | Copper or optical fibre cables, 2,4 ghz network |


### Application layer
Protocols that enable applications to communicate and exchange **application specific** data.

The application layer performs the functions of the three top layers of the OSI model (5,6,7 / Session Presentation, Application). Therefore this layer might be referenced as *layer 7*.

It enables node-to-node communication and controls user-interface specifications. Typical protocols used are SSH, HTTP, FTP or SMTP among others.

- **PDU (Protocol data unit)**: application specific data
- **Unique identifier**: {protocol, local IP address, local port, remote IP address, remote
   port}

### Transport layer
Enables end-to-end communication between hosts.

- **PDU (Protocol data unit)**: segmet
- **Unique identifier**: {local IP address, local port, remote IP address, remote
   port}

### Network layer
Cares about the routing of packets. Point-to-Point connections. Each nodes only cares about the next destination for the packet.

- **PDU (Protocol data unit)**: datagram

### Data Link layer
The data link layer defines the format of data on the network. Control of how data is handled by the physical media through MAC (Media Access Control) and detection of errors.

- **PDU (Protocol data unit)**: frame

### Physical layer
Responsible for transmitting the data over the different types of physical media that may be present. 

- **PDU (Protocol data unit)**: bit

## Ephemeral port

An **ephemeral port** is a communications endpoint ([port](https://en.wikipedia.org/wiki/Port_(computer_networking) "Port (computer networking)")) of a [transport layer](https://en.wikipedia.org/wiki/Transport_layer "Transport layer") protocol of the [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite "Internet protocol suite") that is used for only a short period of time for the duration of a communication session. It is temporary and only valid for the duration of the communication session.



