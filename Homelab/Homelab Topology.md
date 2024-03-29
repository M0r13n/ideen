# Homelab

The homelab consists of:

- a Mikrotik RB3011 Routerboard
- a Mikrotik CRS326 Cloud Router Switch
- a Mikrotik RB260GS PoE Switch


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
| TNG  | 07      | dynamic         |

## RB3011

The following command should be applied to a RB3011 in **default configuration!**

Notes:

- the default bridge is named `bridge` and not something like `bridge`
- my ISP requires authentication over PPPoE on VLAN 7 (tagged)

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
# PPPoE settings
#######################################
# Tag all traffic on ether1 with the VLAN-ID 7
/interface/vlan add vlan-id=7 interface=ether1 name=TNG_VLAN

/interface pppoe-client
add add-default-route=yes  allow=pap,chap,mschap2 disabled=no interface=TNG_VLAN name=TNG use-peer-dns=yes user="foobar"

/interface list member
add comment=defconf interface=ether1 list=WAN
add comment="PPPoE TNG" interface=TNG list=WAN

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

Afterwards it might be a good idea to look at [hardening](Mikrotik%20Security%20Manual.md).

## CRS326

```bash
# jan/04/2023 12:53:51 by RouterOS 7.6
# software id = JLXN-PEZN
#
# model = CRS326-24G-2S+
# serial number = XXXXXXXXXXX

# Create new bridge with VLAN filtering
/interface bridge add admin-mac=DC:2C:6E:D0:90:A5 auto-mac=no comment=defconf ingress-filtering=no name=bridge vlan-filtering=yes

# Auto negotiation fails in my case -> force it to 1 Gbit/s
/interface ethernet
set [ find default-name=sfp-sfpplus1 ] auto-negotiation=no

# Define the three VLANS
/interface vlan
add interface=bridge name=BASE_VLAN vlan-id=99
add interface=bridge name=FAMILY_VLAN vlan-id=20
add interface=bridge name=PROD_VLAN vlan-id=10

# Configure VLAN lists for easier management
/interface list
add name=MGM

/interface list member
add interface=BASE_VLAN list=MGM
add interface=PROD_VLAN list=MGM

# Add all ports to the bridge.
# All ports expect the SFP port are configured as access ports.
# The SFP port is configured as a trunk.
/interface bridge port
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether1 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether2 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether3 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether4 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether5 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether6 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether7 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether8 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether9 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether10 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether11 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether12 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether13 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether14 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether15 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether16 pvid=10
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether17 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether18 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether19 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether20 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether21 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether22 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether23 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-untagged-and-priority-tagged interface=ether24 pvid=20
add bridge=bridge comment=defconf frame-types=admit-only-vlan-tagged interface=sfp-sfpplus1
add bridge=bridge comment=defconf disabled=yes interface=sfp-sfpplus2

# Only listen on the trusted network
/ip neighbor discovery-settings
set discover-interface-list=MGM

# Tell the switch to tag all frames going into SFP1
/interface bridge vlan
add bridge=bridge tagged=sfp-sfpplus1,bridge vlan-ids=99
add bridge=bridge tagged=sfp-sfpplus1 vlan-ids=10
add bridge=bridge tagged=sfp-sfpplus1 vlan-ids=20

# Configure a static IP address
/ip address
add address=192.168.1.2/24 interface=BASE_VLAN network=192.168.1.0
/ip dns
set servers=192.168.1.1
/ip route
add disabled=no dst-address=0.0.0.0/0 gateway=192.168.1.1 routing-table=main suppress-hw-offload=no

# Disable unused services
/ip service
set telnet address=192.168.1.0/24,10.0.10.0/24 disabled=yes
set ftp address=192.168.1.0/24,10.0.10.0/24 disabled=yes
set www address=192.168.1.0/24,10.0.10.0/24 disabled=yes
set ssh address=192.168.1.0/24,10.0.10.0/24
set www-ssl address=192.168.1.0/24,10.0.10.0/24
set api address=192.168.1.0/24,10.0.10.0/24 disabled=yes
set winbox address=192.168.1.0/24,10.0.10.0/24
set api-ssl address=192.168.1.0/24,10.0.10.0/24

# Misc stuff for security and time zone
/ip ssh
set strong-crypto=yes
/system clock
set time-zone-name=Europe/Berlin
/system identity
set name=Boromir
/system ntp client
set enabled=yes
/system ntp client servers
add address=time.cloudflare.com
/system routerboard settings
set boot-os=router-os
/system swos
set address-acquisition-mode=static allow-from-ports=p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26 identity=Boromir static-ip-address=\
    192.168.1.2
/tool bandwidth-server
set enabled=no
/tool mac-server
set allowed-interface-list=MGM
/tool mac-server mac-winbox
set allowed-interface-list=MGM
```

## WAP

```bash
# dec/11/2022 12:29:35 by RouterOS 7.6
/interface bridge
add  auto-mac=no comment="vlan enabled" ingress-filtering=no name=bridgeLocal vlan-filtering=yes

/interface vlan
add interface=bridgeLocal name=BASE_VLAN vlan-id=99
add interface=bridgeLocal name=PROD_VLAN vlan-id=10
add interface=bridgeLocal name=FAMILY_VLAN vlan-id=20

/interface list
add name=MGM

/interface wifiwave2 security
add authentication-types=wpa2-psk,wpa3-psk disable-pmkid=yes encryption=ccmp,gcmp,ccmp-256,gcmp-256 group-encryption=ccmp name=secdef
add authentication-types=wpa2-psk,wpa3-psk disable-pmkid=yes encryption=ccmp,gcmp,ccmp-256,gcmp-256 name=secguest

/interface wifiwave2 configuration
add chains=0,1,2,3 channel.skip-dfs-channels=10min-cac country=Germany mode=ap name=4x5ghz security=secdef ssid="Make Tyrion great again" tx-chains=0,1,2,3
add chains=0,1 channel.skip-dfs-channels=10min-cac country=Germany mode=ap name=2x5ghz security=secdef ssid="Tyrion WLANister 5G" tx-chains=0,1
add chains=0,1 country=Germany mode=ap name=2x2ghz security=secdef ssid="Tyrion WLANister" tx-chains=0,1
add mode=ap name=2x2ghz-quest security=secguest ssid="Einbrecher hier rein"

/interface wifiwave2
set [ find default-name=wifi1 ] configuration=2x2ghz configuration.mode=ap disabled=no
set [ find default-name=wifi2 ] configuration=2x5ghz configuration.mode=ap disabled=no
set [ find default-name=wifi3 ] configuration=4x5ghz configuration.mode=ap disabled=no
add configuration=2x2ghz-quest configuration.mode=ap disabled=no master-interface=wifi1 name=wifi4

/interface bridge port
add bridge=bridgeLocal comment=defconf frame-types=admit-only-vlan-tagged interface=ether1 trusted=yes
add bridge=bridgeLocal comment=prod frame-types=admit-only-untagged-and-priority-tagged interface=ether2 pvid=10
add bridge=bridgeLocal frame-types=admit-only-untagged-and-priority-tagged interface=wifi3 pvid=10
add bridge=bridgeLocal frame-types=admit-only-untagged-and-priority-tagged interface=wifi2 pvid=10
add bridge=bridgeLocal frame-types=admit-only-untagged-and-priority-tagged interface=wifi1 pvid=10
add bridge=bridgeLocal frame-types=admit-only-untagged-and-priority-tagged interface=wifi4 pvid=20

/ip neighbor discovery-settings
set discover-interface-list=MGM

/interface bridge vlan
add bridge=bridgeLocal tagged=ether1,bridgeLocal vlan-ids=99
add bridge=bridgeLocal tagged=ether1 vlan-ids=10
add bridge=bridgeLocal tagged=ether1 vlan-ids=20

/interface list member
add interface=BASE_VLAN list=MGM
add interface=PROD_VLAN list=MGM
add interface=FAMILY_VLAN list=MGM

/ip dhcp-client
add comment=defconf interface=bridgeLocal

/ip dns
set servers=192.168.1.1

/ip route
add disabled=no dst-address=0.0.0.0/0 gateway=192.168.1.1

/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set api disabled=yes
set api-ssl disabled=yes

/ip ssh
set strong-crypto=yes
/system clock
set time-zone-name=Europe/Berlin
/system identity
set name=Eowen
/system ntp client
set enabled=yes
/system ntp client servers
add address=time.cloudflare.com
/tool bandwidth-server
set enabled=no
/tool mac-server
set allowed-interface-list=MGM
/tool mac-server mac-winbox
set allowed-interface-list=MGM
```