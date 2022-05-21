## Subnet masks

- use to determine the **network and host portion** of an address
	-> is the device on the same network or on a remote network?
	-> does the packet has to be routed through a default gateway?
- the network portion is identified through a net mask
- the netmask is a binary mask that is binary ANDed with the destination address

## CIDR (Classless Inter-Domain Routing)
- replaces class A,B,C netwoks
- `/X` mask, where `X` tell the number of leading binary 1s
	-> /8 equals `11111111.00000000.00000000.00000000` which equals `255.0.0.0`
	 -> /16 equals `11111111.11111111.00000000.00000000` which equals `255.255.0.0`
	 -> /24 equals `11111111.11111111.11111111.00000000` which equals `255.255.255.0`
- what is the problem with class based networks?
	- too inflexible
	- there are:
		- class A networks have ~ 16 million addresses
		- class B networks have 65534 addresses
		- class C networks have 254 addresses
	* if I need 3000 addresses I can either:
		* get a class B network and waste thousands of addresses
		* get multiple class C networks and cause a lot of  additional entries in routing tables, because each network has to be individually propagated
		- instead I can assign  /20 network (e.g `192.168.0.1/24`)
