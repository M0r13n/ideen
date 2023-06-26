- **LAG (Link Aggregation Protocol):** joins multiple physical links to a single logical link
- **MLAG (Multiple-Chassis Link Aggregation):** extension of LAG. Adds node-level redundancy to the normal link-level redundancy that a LAG provides (multiple switches)
- **LACP (Link Aggregation Control Protocol):** protocol for dynamic LAGs

![[mlag.png]]
### LACP

- **link aggregation group** (**LAG**) is the combined collection of physical ports
- https://en.wikipedia.org/wiki/Link_aggregation#802.1AX
- can be configured in different ways
	- round robin for more bandwith
	- active-backup for redundancy
	- and more
- L2 or L3 hashes may be used to prevent packet reordering
	- the same flow is always sent via the same physical link

### MLAG

- multiple vendor specific proprietary implementations
- not interoperable
