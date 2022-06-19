# My Vision

I want to split my network into two [VLANs](#TBD) + a dedicated Management VLAN (native VLAN) for backup.

I envisioned the following VLANs:

- MGM: backup VLAN in case anything happens
- PROD: Production VLAN for all my trusted devices (Workstation, Laptop, NAS)
- FAM: Family VLAN for stuff that I do not fully control (IoT, Guests, Family members, Printers, Smartphones, IP-Cameras)

I think about the following setup:

| VLAN | VLAN ID | Network | Router | DHCP |
| ---  | ---     | ---     | ---    | ---  |
| MGM  | 1       | 10.0.1.0\24 | 10.0.1.1 | no |
| PROD | 10      | 10.0.10.0\24| 10.0.10.1 | yes |
| FAM  | 20      | 10.0.20.0\24| 10.0.20.1 | yes |


## ER X config

```bash
configure

########################
# INTERFACES           #
########################
set interfaces switch switch0 vif 10 address 10.0.10.1/24
set interfaces switch switch0 vif 20 address 10.0.20.1/24

########################
# DHCP                 #
########################

# Create DHCP server config for PROD (10.0.10.11 - 10.0.10.250)
set service dhcp-server shared-network-name vlan10 subnet 10.0.10.0/24 start 10.0.10.11 stop 10.0.10.250
set service dhcp-server shared-network-name vlan10 subnet 10.0.10.0/24 default-router 10.0.10.1
set service dhcp-server shared-network-name vlan10 subnet 10.0.10.0/24 dns-server 10.0.10.1

# Create DHCP server config for FAM (10.0.20.11 - 10.0.20.250)
set service dhcp-server shared-network-name vlan20 subnet 10.0.20.0/24 start 10.0.20.11 stop 10.0.20.250
set service dhcp-server shared-network-name vlan20 subnet 10.0.20.0/24 default-router 10.0.20.1
set service dhcp-server shared-network-name vlan20 subnet 10.0.20.0/24 dns-server 10.0.20.1

########################
# PORT CONFIG          #
########################
set interfaces switch switch0 switch-port vlan-aware enable

# Make eth1 tagged for PROD_VLAN and untagged for FAM_VLAN
set interfaces switch switch0 switch-port interface eth1 vlan pvid 20
set interfaces switch switch0 switch-port interface eth1 vlan vid 10

# Make eth2 tagged for PROD_VLAN and untagged for FAM_VLAN
set interfaces switch switch0 switch-port interface eth2 vlan pvid 20
set interfaces switch switch0 switch-port interface eth2 vlan vid 10

# Make eth3 untagged for FAM_VLAN
set interfaces switch switch0 switch-port interface eth3 vlan pvid 20

########################
# DNS                  #
########################

# Increase the default cache size
set service dns forwarding cache-size 1000

# Tell the DNS server listen on the newly created interfaces
set service dns forwarding listen-on switch0.10
set service dns forwarding listen-on switch0.20


########################
# Portgroup            #
########################
set firewall group port-group ROUTER_ACCESS port ssh
set firewall group port-group ROUTER_ACCESS port https
set firewall group port-group ROUTER_ACCESS port telnet


########################
# FIREWALL Rules       #
########################

# Note:
# IN:       Traffic coming from the VLAN into the EdgeRouter
# OUT:      Traffic going out of the EdgeRouter and into the VLAN
# LOCAL:    Traffic on the VLAN itself (broadcasts, multicast, unicast).\

# Prevent guests from managing the Edgerouter
set firewall name FAM_LOCAL default-action accept

set firewall name FAM_LOCAL rule 10 action drop
set firewall name FAM_LOCAL rule 10 description "Deny traffic from FAM to edgerouter"
set firewall name FAM_LOCAL rule 10 log disable
set firewall name FAM_LOCAL rule 10 destination group port-group ROUTER_ACCESS
set firewall name FAM_LOCAL rule 10 destination address 10.0.20.1

# Allow Internet access but deny traffic from FAM to PROD
set firewall name FAM_IN default-action accept

# Allow Established/Related
set firewall name FAM_IN rule 10 action accept
set firewall name FAM_IN rule 10 description "Accept Established/Related"
set firewall name FAM_IN rule 10 log disable
set firewall name FAM_IN rule 10 protocol all
set firewall name FAM_IN rule 10 state established enable
set firewall name FAM_IN rule 10 state related enable

# Any exception (e.g. allow traffic to a web server need to be added before the drop rule)

# Drop everything from FAM to PROD
set firewall name FAM_IN rule 20 action drop
set firewall name FAM_IN rule 20 description "Deny traffic from FAM to PROD"
set firewall name FAM_IN rule 20 log disable
set firewall name FAM_IN rule 20 protocol all
set firewall name FAM_IN rule 20 destination address 10.0.10.0/24

set interfaces switch switch0 vif 20 firewall in name FAM_IN
set interfaces switch switch0 vif 20 firewall local name FAM_LOCAL


commit ; save
```

## Resources

- https://www.geekbitzone.com/posts/networking/vlans/vlan-edgerouter-mikrotik/edgerouter-mikrotik-swos-vlan/#setting-up-firewall-policies-on-the-edgerouter
- https://help.ui.com/hc/en-us/articles/115012700967-EdgeRouter-VLAN-Aware-Switch
- https://help.ui.com/hc/en-us/articles/218889067-EdgeRouter-How-to-Create-a-Guest-LAN-Firewall-Rule