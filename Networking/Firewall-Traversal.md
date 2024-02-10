# How to establish a bidirectional communication through firewalls?

**Assumptions:**

1. Both devices are controlled by the same entity
2. In between firewalls are not controlled by the entity
3. In between firewalls allow outbound traffic, but block inbound traffic
4. Firewalls only consider `(src-ip, src-port, dst-ip, dst-port)`
5. UDP or QUIC is used as the transport layer protocol
6. There is sidechannel to exchange _some_ information

**Problem**:

Hen and egg problem: **Both sides have to go first, but neither side can go first, because the other side has to go first.**

![The problem with firewalls](../assets/problem.svg)

**Solution:**

![How to establish a 2-way communication channel](../assets/solution.svg)

- both entities agree on source and destination ports via a sidechannel
- A tries to connect to B on port `5555`
- this packet is dropped by F2, because there is no recent packet
- B answers anyway to port `4444` and sets is source port to `5555`
- this packet is accepted by F1, because it has seen a matching packet
- A responds again with the same ports
- F2 now accepts the packet, because it has seem a matching one
- [more details](https://tailscale.com/blog/how-nat-traversal-works)