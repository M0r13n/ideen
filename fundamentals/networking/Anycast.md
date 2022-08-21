# Anycast

Anycast works like Unicast in the sense that a **single** packet is delivered to a **single** destination host.
The crucial difference is that there are multiple physical machines sharing the same destination address.
The packet is delivered to the host that is **closest to the sender** (shortest route).

- less latency than Unicast
- better availability than Unicast
- based on the BGB routing protocol

Anycast works like buying a (smart)phone in real life.
It is possible to buy the same smartphone in many different stores.
In general I am going to buy in a shop that is geographically nearest store.
But if the store is closed I am able to drive a bit further and still buy the phone.

On the WAN the final destination is chosen based on the shortest path from sender to recipient.

Anycast works with UDP out of the box.
It is therefore widely used by DNS oder streaming services.
Stateful protocols require carefully crafted routes to prevent flapping.
The TCP three-way handshake requires all packets to hit the same recipient.

