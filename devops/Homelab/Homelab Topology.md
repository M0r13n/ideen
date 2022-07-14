# Homelab

The homelab consists of:

- a Mikrotik RB3011 Routerboard
- a Mikrotik CRS326 Cloud Router Switch
- a Mikrotik RB260GS PoE Switch
- multiple Ubiquiti Edgerouter X

## Topology

```txt
                                                                                           ┌────────────────────────────────────────┐
                                                                                           │                                        │
                                                                                           │                Legend                  │
  ┌────────────────────────────────────────────────────────────────────────┐               │                                        │
  │                                RB3011                                  │               │                                        │
  │                                                                        │               │    W = WAN                             │
  │   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐    │               │    T = Trunk All                       │
  │   │ T │ │ W │ │ T │ │ T │ │ T │ │ T │ │ T │ │ T │ │ T │ │ T │ │ T │    │               │                                        │
  │   └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘    │               │    m = Access Port Management VLAN     │
  │    SFP  eth1  eth2  eth3  eth4  eth5  eth6  eth7  eth8  eth9  eth10    │               │    p = Access Port Production          │
  └─────┬──────────────────────────────────────────────────────────────────┘               │    f = Access Port Family              │
        │                                                                                  │                                        │
        │                                                                                  │                                        │
        │                                                                                  │    D = Disabled                        │
        │                                                                                  └────────────────────────────────────────┘
        │
        │                                        1G
        └─────────────────────────────────────────────────────────────────────────────────────────┐
                                                                                                  │
                                                                                                  │
                                                                                                  │
                                                                                                  │
                                                                                                  │
┌─────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────┐
│                                                                                                 │                            │
│                                           CRS326                                                │                            │
│                                                                                                 │                            │
│     ┌───┐   ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐         │                            │
│     │ p │   │ p │  │ p │  │ p │  │ p │  │ p │  │ p │  │ p │  │ f │  │ f │  │ f │  │ f │         │                            │
│     └───┘   └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘         │                            │
│     eth1    eth3   eth5   eth7   eth9   eth11  eth13  eth15  eth17  eth19  eth21  eth23     ┌───┴───┐    ┌───────┐           │
│                                                                                             │   T   │    │   T   │           │
│     ┌───┐   ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐     └───────┘    └───────┘           │
│     │ p │   │ p │  │ p │  │ p │  │ p │  │ p │  │ p │  │ p │  │ f │  │ f │  │ f │  │ m │        SFP1         SFP2             │
│     └───┘   └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘  └───┘                                      │
│     eth2    eth4   eth6   eth8   eth10  eth12  eth14  eth16  eth18  eth20  eth22  eth24                                      │
│                                                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## VLAN Table

| VLAN | VLAN ID | Network         |
| ---  | ---     | ---             |
| PROD | 10      | 10.0.10.0\24    |
| FAM  | 20      | 10.0.20.0\24    |
| MGM  | 99      | 192.168.1.1\24  |

## Configuration (CLI)

The following command should be applied to a RB3011 in **default configuration!**

Notes:

- the default bridge is named `bridge` and not something like `bridge`

```bash
#######################################
# Bridge
#######################################

# create one bridge, set VLAN mode off while we configure
/interface bridge set vlan-filtering=no [find name=bridge]

#######################################
# -- Trunk Ports --
#######################################

# egress behavior
/interface bridge vlan

# Purple Trunk. These need IP Services (L3), so add Bridge as member
add bridge=bridge tagged=bridge,ether2,ether3,ether4,ether5,ether6,ether7,ether8,ether9,ether10,sfp1 vlan-ids=10
add bridge=bridge tagged=bridge,ether2,ether3,ether4,ether5,ether6,ether7,ether8,ether9,ether10,sfp1 vlan-ids=20
add bridge=bridge tagged=bridge,ether2,ether3,ether4,ether5,ether6,ether7,ether8,ether9,ether10,sfp1 vlan-ids=99


#######################################
# IP Addressing & Routing
#######################################

# LAN facing router's IP address on the BASE_VLAN
/interface vlan add interface=bridge name=BASE_VLAN vlan-id=99
/ip address add address=192.168.1.1/24 interface=BASE_VLAN

# DNS server, set to cache for LAN
# See ./Mikrotik DoH.md for DNS over HTTPS
/ip dns set allow-remote-requests=yes servers="9.9.9.9"

#######################################
# IP Services
#######################################

# PROD VLAN interface creation, IP assignment, and DHCP service
/interface vlan add interface=bridge name=PROD_VLAN vlan-id=10
/ip address add interface=PROD_VLAN address=10.0.10.1/24
/ip pool add name=PROD_POOL ranges=10.0.10.2-10.0.10.254
/ip dhcp-server add address-pool=PROD_POOL interface=PROD_VLAN name=PROD_DHCP disabled=no
/ip dhcp-server network add address=10.0.10.0/24 dns-server=192.168.1.1 gateway=10.0.10.1

# FAMILY VLAN interface creation, IP assignment, and DHCP service
/interface vlan add interface=bridge name=FAMILY_VLAN vlan-id=20
/ip address add interface=FAMILY_VLAN address=10.0.20.1/24
/ip pool add name=FAMILY_POOL ranges=10.0.20.2-10.0.20.254
/ip dhcp-server add address-pool=FAMILY_POOL interface=FAMILY_VLAN name=FAMILY_DHCP disabled=no
/ip dhcp-server network add address=10.0.20.0/24 dns-server=192.168.1.1 gateway=10.0.20.1

# Create a DHCP pool for the BASE VLAN to make administration a bit less painful
/ip pool add name=BASE_POOL ranges=192.168.1.10-192.168.1.254
/ip dhcp-server add address-pool=BASE_POOL interface=BASE_VLAN name=BASE_DHCP disabled=no
/ip dhcp-server network add address=192.168.1.0/24 dns-server=192.168.1.1 gateway=192.168.1.1


#######################################
# Firewall
#######################################
# Remove the LAN list which comes by default
/interface list remove [find name=LAN]

# Create two interface lists
/interface list add name=MGM
/interface list add name=VLAN

# Add all VLANs as members
/interface list member

add interface=BASE_VLAN   list=VLAN
add interface=PROD_VLAN   list=VLAN
add interface=FAMILY_VLAN list=VLAN
add interface=BASE_VLAN list=MGM
add interface=PROD_VLAN list=MGM

#######################################
# IPV4
#######################################
/ip firewall filter

# Remove all firewall rules that come pre configured
remove [find dynamic=no]

# Input-Chain: Packets that are going into the router
add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
add chain=input action=drop connection-state=invalid comment="defconf: drop invalid"
add chain=input action=accept protocol=icmp comment="defconf: accept ICMP"
# add chain=input action=accept dst-address=127.0.0.1 comment="defconf: accept to local loopback (for CAPsMAN)"
add chain=input action=accept in-interface-list=VLAN comment="Allow VLAN to access DNS on this router" protocol=udp port=53
add chain=input action=accept in-interface-list=MGM comment="Allow MGM VLANs full access to this router"
add chain=input action=drop comment="Drop everything else"

# Forward-Chain: Packets forwarded by the router
add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept in ipsec policy"
add chain=forward action=accept ipsec-policy=out,ipsec comment="defconf: accept out ipsec policy"
add chain=forward action=fasttrack-connection connection-state=established,related comment="defconf: fasttrack"
add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related, untracked"
add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid"
add chain=forward action=accept connection-state=new in-interface-list=VLAN out-interface-list=WAN comment="Allow VLANs to access the Internet"
add chain=forward action=accept connection-state=new in-interface-list=MGM out-interface-list=VLAN comment="Allow MGM to access ALL other VLANS"
add chain=forward action=drop comment="Drop everything else"

#######################################
# IPV6
#######################################
/ipv6 firewall address-list

remove [find comment~"defconf"]

add list=bad_ipv6 address=::/128 comment="defconf: unspecified address"
add list=bad_ipv6 address=::1 comment="defconf: lo"
add list=bad_ipv6 address=fec0::/10 comment="defconf: site-local"
add list=bad_ipv6 address=::ffff:0:0/96 comment="defconf: ipv4-mapped"
add list=bad_ipv6 address=::/96 comment="defconf: ipv4 compat"
add list=bad_ipv6 address=100::/64 comment="defconf: discard only "
add list=bad_ipv6 address=2001:db8::/32 comment="defconf: documentation"
add list=bad_ipv6 address=2001:10::/28 comment="defconf: ORCHID"
add list=bad_ipv6 address=3ffe::/16 comment="defconf: 6bone"

/ipv6 firewall filter

remove [find dynamic=no]

add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
add chain=input action=drop connection-state=invalid comment="defconf: drop invalid"
add chain=input action=accept protocol=icmpv6 comment="defconf: accept ICMPv6"
add chain=input action=accept protocol=udp port=33434-33534 comment="defconf: accept UDP traceroute"
add chain=input action=accept protocol=udp dst-port=546 src-address=fe80::/10 comment="defconf: accept DHCPv6-Client prefix delegation."
add chain=input action=accept protocol=udp dst-port=500,4500 comment="defconf: accept IKE"
add chain=input action=accept protocol=ipsec-ah comment="defconf: accept ipsec AH"
add chain=input action=accept protocol=ipsec-esp comment="defconf: accept ipsec ESP"
add chain=input action=accept ipsec-policy=in,ipsec comment="defconf: accept all that matches ipsec policy"
add chain=input action=accept in-interface-list=VLAN comment="Allow VLAN to access DNS on this router" protocol=udp port=53
add chain=input action=accept in-interface-list=MGM comment="Allow MGM VLANs full access to this router"
add chain=input action=drop comment="Drop everything else"

add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid"
add chain=forward action=drop src-address-list=bad_ipv6 comment="defconf: drop packets with bad src ipv6"
add chain=forward action=drop dst-address-list=bad_ipv6 comment="defconf: drop packets with bad dst ipv6"
add chain=forward action=drop protocol=icmpv6 hop-limit=equal:1 comment="defconf: rfc4890 drop hop-limit=1"
add chain=forward action=accept protocol=icmpv6 comment="defconf: accept ICMPv6"
add chain=forward action=accept protocol=139 comment="defconf: accept HIP"
add chain=forward action=accept protocol=udp dst-port=500,4500 comment="defconf: accept IKE"
add chain=forward action=accept protocol=ipsec-ah comment="defconf: accept ipsec AH"
add chain=forward action=accept protocol=ipsec-esp comment="defconf: accept ipsec ESP"
add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept all that matches ipsec policy"
add chain=forward action=accept connection-state=new in-interface-list=VLAN out-interface-list=WAN comment="Allow VLANs to access the Internet"
add chain=forward action=accept connection-state=new in-interface-list=MGM out-interface-list=VLAN comment="Allow MGM to access ALL other VLANS"
add chain=forward action=drop comment="Drop everything else"

#######################################
# VLAN Security
#######################################

# Only allow packets with tags over the Trunk Ports
/interface bridge port
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether2]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether3]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether4]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether5]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether6]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether7]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether8]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether9]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=ether10]
set bridge=bridge ingress-filtering=yes frame-types=admit-only-vlan-tagged [find interface=sfp1]

# Only allow users to sign in from MGM subnets
/user set [find] address=192.168.1.0/24,10.0.10.0/24

#######################################
# MAC Server settings
#######################################

# Ensure only visibility and availability from BASE_VLAN, the MGMT network
/ip neighbor discovery-settings set discover-interface-list=MGM
/tool mac-server mac-winbox set allowed-interface-list=MGM
/tool mac-server set allowed-interface-list=MGM

#######################################
# Turn on VLAN mode
#######################################
/interface bridge set bridge vlan-filtering=yes

#######################################
# Cleanup Defaults
#######################################
# Remove default address 192.168.88.1
/ip address remove [find network=192.168.88.0]

# Remove default DHCP server
/ip pool remove [find name="default-dhcp"]
/ip dhcp-server/ remove [find name="defconf"]

# Deactivate unused IP services
/ip service 
disable telnet,ftp
set [find] address=192.168.1.0/24,10.0.10.0/24

```

Afterwards it might be a good idea to look at [hardening](./Mikrotik%20Security%20Manual.md).

## CAPsMAN

Router: 

```bash

/caps-man configuration add country=germany name=Config-2G security.authentication-types=wpa2-psk security.passphrase=top_secret security.encryption=aes-ccm security.group-encryption=aes-ccm ssid=Baba-Netz channel.band=2ghz-b/g/n datapath.local-forwarding=yes datapath.vlan-id=10 datapath.vlan-mode=use-tag datapath.client-to-client-forwarding=yes 

/caps-man provisioning  add action=create-dynamic-enabled master-configuration=Config-2G hw-supported-modes=gn

/caps-man configuration add country=germany name=Config-5G security.authentication-types=wpa2-psk security.passphrase=top_secret security.encryption=aes-ccm security.group-encryption=aes-ccm datapath.client-to-client-forwarding=yes ssid=Baba-Netz-5 channel.band=5ghz-n/ac datapath.local-forwarding=yes datapath.vlan-id=10 datapath.vlan-mode=use-tag

/caps-man provisioning add action=create-dynamic-enabled master-configuration=Config-5G hw-supported-modes=an,ac

/caps-man manager interface
set [ find default=yes ] forbid=yes
add disabled=no interface=BASE_VLAN

# Improve roaming by kicking clients off of weak APs
/caps-man access-list
add action=reject interface=any signal-range=-120..-88

```

### WAP

```bash

# Temporarily disable VLAN filtering while configuring
/interface bridge
set vlan-filtering=no [find name=bridge]

#######################################
# VLAN Configuration
#######################################
# Remove default List
/interface list remove [find name=LAN]

# Add the Base VLAN with ID 99 (adjust to match Base VLAN)
/interface vlan add interface=bridge name=BASE_VLAN vlan-id=99
/interface vlan add interface=bridge name=PROD_VLAN vlan-id=10

# Create two interface lists
/interface list add name=MGM

# Add all VLANs as members
/interface list member

add interface=BASE_VLAN list=MGM
add interface=PROD_VLAN list=MGM

#######################################
# VLAN Ingress
#######################################
/interface bridge port

# Configure Ether1 as a Trunk port
add bridge=bridge interface=ether1 trusted=yes frame-types=admit-only-vlan-tagged ingress-filtering=yes comment="trunk"

# Configure Ether2 as a Prod port (VLAN-ID 10)
add bridge=bridge interface=ether2 pvid=10 frame-types=admit-only-untagged-and-priority-tagged ingress-filtering=yes comment="prod"


#######################################
# VLAN Egress
#######################################
/interface bridge vlan
add bridge=bridge tagged=ether1,bridge  vlan-ids=99
add bridge=bridge tagged=ether1         vlan-ids=10
add bridge=bridge tagged=ether1         vlan-ids=20

#######################################
# IP configuration
#######################################

# Local Static IP on the Base VLAN
# NOTE: Adjust the IP for each device!
/ip address add interface=BASE_VLAN address=192.168.1.4/24
/ip route add distance=1 gateway=192.168.1.1
/ip dns set servers=192.168.1.1

#######################################
# CAPsMAN mode
#######################################
/interface wireless cap
set bridge=bridge discovery-interfaces=BASE_VLAN caps-man-addresses=192.168.1.1 enabled=yes interfaces=wlan1,wlan2,wlan3
set certificate=none

#######################################
# Configuration Services
#######################################
# Ensure only visibility and availability from BASE_VLAN, the MGMT network
/tool mac-server mac-winbox set allowed-interface-list=MGM
/tool mac-server set allowed-interface-list=MGM
/tool bandwidth-server set enabled=no

/ip neighbor discovery-settings set discover-interface-list=MGM
/ip service disable telnet,ftp,www,api,api-ssl
/ip proxy set enabled=no
/ip socks set enabled=no
/ip upnp set enabled=no
/ip cloud set ddns-enabled=no update-time=no
/ip ssh set strong-crypto=yes

#######################################
# Turn on VLAN mode
#######################################
/interface bridge set BR1 vlan-filtering=yes comment="vlan enabled"

```