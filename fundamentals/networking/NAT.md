# Network Address Translation (NAT)

- allows multiple hosts to share a single public IP behind a gateway
- operates on **Layer 3**
- **Source-NAT**: changes the source IP in the packet header and optionally the source port
  - **Masquerading**: the router rewrites the source ip automatically - the client does not know about the NATing
- **Destination-NAT**: changes the destination IP in the packet header and optionally the destination port
  - works like port forwarding in TCP/UDP

## Source NAT

```mermaid
graph LR
    Client -->|192.168.0.2 : 10101 | Router
    Router --> Client

    Router -->|220.0.0.1 : 20202 | Server
    Server --> Router

```

- the private RFC1918 network is `192.168.0.2/24`
- the router is publicly accessible via `220.0.0.1`
- the client wants to communicate with a remote server

1. a client crafts an IP packet:
    - source ip: 192.168.0.2
    - dest ip: Server IP
    - src port: 10101
    - dst port: Server port
2. the client looks into his routing table and sends the packet to its default gateway
3. the NAT router replaces the private src address with its address and swaps the src port with a random port and saves a mapping in his NAT table
    - source ip: 220.0.0.1
    - dest ip: Server IP
    - src port: 20202
    - dst port: Server port
4. the router passes the packet to the next router
5. the server receives the packet and crafts a response
6. the packet is routed to the clients network router
7. the router takes a look into his NAT table and determines the client to which the packet should be delivered
8. the router swaps the dst port and dst port to match the original packet
