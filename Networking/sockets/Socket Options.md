# Socket Options

### SO_REUSEADDR

-> allows to bind to a socket even if another socket socket is in `TIME_WAIT`
	- only relevant for TCP sockets
	- t==he last ACK of the FIN-ACK disconnect might get lost==
	- so a remote peer might consider the local socket as open, even so it was already closed
	- therefore, by default the Kernel puts the closed socket into `TIME_WAIT`
	- the duration can vary between a couple of **seconds and minutes**
	- as long as a socket is in `TIME_WAIT` no other socket can bind to the same source address and source port
	- `SO_REUSEADDR` simply ignores and existing sockets in `TIME_WAIT`
-> changes how wildcard addresses are treated in ==regards to conflicts==
	- the same source address and source port combination can not be used by two sockets
	- each socket needs to bind to a unique combination of `(source address, source port)`
	- `0.0.0.0` is a wildcard that matches **ALL** local addresses
		- `127.0.0.1:80` and `127.0.0.2:80` -> O.K.
		- `127.0.0.1:80` and `127.0.0.1:81` -> O.K.
		- `127.0.0.1:80` and `127.0.0.1:80` -> NOT O.K.
		- `0.0.0.0:80` and `127.0.0.1:80` -> NOT O.K. (would be okay with `REUSEADDR`)
		-  `0.0.0.0:80` and `127.0.0.2:80` -> NOT O.K. (s.o.)
- only relevant during `bind()`
- existing sockets are note even looked at
- refer to: https://stackoverflow.com/questions/1694144/can-two-applications-listen-to-the-same-port

### SO_REUSEPORT
-> allows **any number** of sockets to bind to the **same source address and source port**
	- only works if **all prior sockets** have set this flag
	- on Linux all sockets that want to share the same address, port combination need to belong to the same User ID to avoid **port hijacking**
-> can be used as a cheap load balancer, because `SO_REUSEPORT` distributes datagrams evenly across all of the receiving threads
	- incoming datagrams are distributed to the server sockets using ==a hash based on the 4-tuple of the connection==—that is, the peer IP address and port plus the local IP address and port
	- a series of datagrams from the same client socket will all be directed to the same receiving server (as long as it continues to exist)
- refer to: https://lwn.net/Articles/542629/