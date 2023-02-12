# Setup PPPoE with Mikrotik

In my case I am using TNG as my ISP. TNG requires me to use a tagged VLAN (VID 7). I am using the PPPoE protocol to authenticate against my ISP (TNG).

```bash
# Tag all traffic on ether1 with the VLAN-ID 7
/interface/vlan
add vlan-id=7 interface=ether1 name=vlan07

# PPPoE client configuration
/interface pppoe-client
add add-default-route=yes  allow=pap,chap,mschap2 disabled=no interface=vlan07 name=TNG use-peer-dns=yes user="foobar"

# Add both interfaces to the WAN list
# This is needed if you have configured the firewall with interface lists
/interface list member
add comment=defconf interface=ether1 list=WAN
add interface=TNG list=WAN

# Enable SRC NAT
/ip firewall nat
add action=masquerade chain=srcnat comment="defconf: masquerade" ipsec-policy=out,none out-interface-list=WAN
```