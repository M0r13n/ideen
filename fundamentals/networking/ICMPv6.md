# ICMPv6

ICMPv6 is a dedicated protocol that is heavily used by IPv6. Its main purpose is ti provide state information and error messages for IP, TCP and UDP. 

## RA - Router Advertisement

- type 134
- used for SLAAC
- router periodically sends a router advertisement to the Multicast address `ff02::1`
- `Router Advertisement from dc:2c:6f:ff:ff:ff is 2a00::/16`

## RS - Router Solicitation

- type 135
- used by hosts to ask a router for a router advertisement
- used if the host does not want to wait for the next router advertisement

## Neighbor Advertisement

- type 136
- answer to Neighbor Solicitations
- `Neighbor Advertisment 2a00::ffff:ffff:ffff:ffff is at ff:ff:ff:ff:ff:ff `

## Neighbor Solicitation

- type 137
- used for Duplicate Address Detection
- *does anyone use this address? Please answer!*

## Neighbor Cache

- works like the ARP Cache in IPv4
- remembers the all known neighbors in the local network
- `ip -6 ns` (Linux)
- `netsh interface ipv6 show neighbors` (Windows)