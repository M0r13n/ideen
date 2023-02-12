The following rules can be used to calculate the specific address:

- **Network/Subnet address**
	- set all bits of the Host Address Portion to 0
* **Broadcast Address**
	* set all bits of the Host Address Portion to 1
* **First Host Address**
	* set all bits to 0 except for the LSB which is set to 1
- **Last Host Address
	- set all bits to 1 except for the LSB which is set to 0

#### Example

Get the Network, Broadcast, First and Last address for the network of the host `172.16.1.1\18`:

- Network mask: `\18` -> `1111 1111.1111 1111.1100 0000.0000 0000` -> `255.255.192.0`
- Subnet Address:
	- the first two Octets are untouched (16 bits < 18 bits)
	- `1100 0000.0000 0000` (network mask)
	- `00|00 0001.0000 0001` (`1.1` as binary)
	-> the first two bits are network and are always 0
	-> all host bits set to zero
	-> subnet address is `172.16.0.0\18`
- first address
	- `00|00 0000.0000 0001` (all host bits 0 and LSB 1)
	-> `172.16.0.1\18`
- last address
	- `00|11 1111.1111 1110` (all host bits 1 and LSB 0)
	-> `172.16.63.254\18`
- Broadcast Address:
	- `00|11 1111.1111 1111` (all host bits 1)
	-> `172.16.63.255`
