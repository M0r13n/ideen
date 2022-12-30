ICMPv6 is a dedicated protocol that is heavily used by IPv6. Its main purpose is ti provide state information and error messages for IP, TCP and UDP. 

## RA - Router Advertisement

- type 134
- used for SLAAC
- router periodically sends a router advertisement to the Multicast address `ff02::1`
- `Router Advertisement from dc:2c:6f:ff:ff:ff is 2a00::/16`
- used for:
	- prefix information
	- local network parameters such as MTU
	- default gateway

## RS - Router Solicitation

- type 135
- used by hosts to ask a router for a router advertisement
- used if the host does not want to wait for the next router advertisement
- multicast address: `ff02::2`

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

## RA Guard

Any device on the network can send Router Advertisements. There is no mechanism to verify or validate such advertisements. Thus, an attacker could spoof these. An attacker could try to redirect the traffic by manipulating the default gateway or it could cause a denial of service by overloading the devices on the network. The latter could be achieved by sending lots of different advertisements for new prefixes. Such prefix announcements may cause clients to be busy configuring their prefixes.

**IPv6 RA guard** is a feature that <mark>filters routers advertisements on network switches</mark>. Therefore, policies can be defined. Such policies can be simple: *"Never forward RA advertisements on this interface"* or complex: *"only forward this RA advertisement if it matches certain criteria"*.
