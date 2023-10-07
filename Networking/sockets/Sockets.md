## Sockets

A socket ...

	- acts as an endpoint for sending an receiving data
	- provides a programming interface (API)
	- is one endpoint of a two-way communication link between two hosts

A socket is bound to a port number so that the TCP layer can identify the  application that data is destined to be sent to.

Of the various forms of IPC, sockets are by far the most popular.  On any given platform, there are likely to be other forms of IPC that are faster, **but for cross-platform communication, sockets are about the only game in town**.

## SOCK_STREAM vs SOCK_DGRAM

- SOCK_STREAM -> TCP, because it is a bidirectional stream of data
- SOCK_DGRAM -> UDP, because it is sending single datagram