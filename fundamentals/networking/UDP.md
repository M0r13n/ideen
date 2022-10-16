# UDP

- defined in [RFC 768](https://www.ietf.org/rfc/rfc768.txt)
- based in the Internet Protocol (IP) is used on the transport layer
- designed to deliver messages with a minimum of protocol mechanisms
- transaction oriented (stateless)
- delivery is not guaranteed (unreliable)
- no duplicate protection

## UDP Datagram

0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|     Source      |   Destination   |
|      Port       |      Port       |
+--------+--------+--------+--------+
|                 |                 |
|     Length      |    Checksum     |
+--------+--------+--------+--------+
|
|          data octets ...
+---------------- ...

**Source Port**
Port number of the sending process.
Used by the sender to pass answers to the right process.

**Destination Port**
Port number of the receiving process (e.g. 53 port DNS).

**Length**
The length in octets of the user datagram **including header and data**.
The minimum value of the length is eight (8), because the header has a total
of eight bytes (64 bits).


**Checksum**
16-bit one's complement of the one's complement sum of a
pseudo header of information from the IP header, the UDP header, and the
data,  padded  with zero octets  at the end (if  necessary)  to  make  a
multiple of two octets.

The pseudo  header  conceptually prefixed to the UDP header contains the
source  address,  the destination  address,  the protocol,  and the  UDP
length.   This information gives protection against misrouted datagrams.
This checksum procedure is the same as is used in TCP.

**data**
The actual payload/data that is transmitted via UDP.


## Resources

- https://blog.cloudflare.com/everything-you-ever-wanted-to-know-about-udp-sockets-but-were-afraid-to-ask-part-1/
- https://www.ietf.org/rfc/rfc768.txt