# DNS-Based Service Discovery

## Problem Definition

- goal: save unnecessary round trips
- `curl -L "leonmortenrichter.de"`
  - does my domain support HTTPS?
  - curl does not know!
  - it sends a HTTP request to port 80
  - which is redirected (Code 302) to HTTPS
  - additional latency and data leakage
- same applies to HTTP/3
  - does a site support the faster protocol?
  - clients only know after receiving the Alt-Svc headers
  - clients miss out on the fast HTTP/3 on the first visit
- chicken and egg problem: HTTP negotiates its parameters over HTTP

## Service Bindings to the Rescue

- generic “SVCB”  records can be instantiated by records specific to different protocols

- e.g. HTTP

  ```txt
  ;; ANSWER SECTION:
  leonmortenrichter.de.   300     IN      HTTPS   1 . alpn="h3,h2" ipv4hint=104.21.50.215,172.67.167.118 ipv6hint=2606:4700:3031::ac43:a776,2606:4700:3036::6815:32d7
  ```

- Application-Layer Protocol Negotiation (ALPN)

  - `alpn="h3,h2"` => my side support HTTP/2 and HTTP/3

- such records still need to be fetched individually

  - can (should?) be done in parallel

- many different protocol specific use cases exist

  - more likely to come

- RFC 9460 introduced the **SVCB** record

- `SVCB` DNS RR represents a general record for different service types

- `HTTPS` DNS RR is specifically designed to be used with HTTPS

- these are the only two records for this purpose

- alias mode: operator of "http://example.com" could point requests to a server at "svc.example.com": 

  - `example.com. 3600 IN HTTPS 0 svc.example.net`


## In the Wild

- [Source][https://www.net.in.tum.de/fileadmin/bibtex/publications/papers/zirngibl2023svcb.pdf]
- of 400M domains 
  - 4k use SVCB records
  - 10.5M use HTTPS records
  - mostly Cloudflare als ALPN + ipv4-/ipv6hints
- authors used QScanner for QUIC handshakes
- authors used MassDNS for DNS scanning