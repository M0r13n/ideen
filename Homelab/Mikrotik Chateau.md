# Chateau Config

This is my Chateau config for my flat:

```
/interface bridge
add auto-mac=yes comment=defconf name=bridge
/interface lte
# A newer version of modem firmware is available!
set [ find default-name=lte1 ] allow-roaming=no band="" disabled=yes
/interface wireless
set [ find default-name=wlan1 ] band=2ghz-b/g/n channel-width=20/40mhz-XX country=germany disabled=no distance=indoors frequency=auto installation=indoor mode=ap-bridge ssid=Nebuchadnezzar \
    wireless-protocol=802.11
set [ find default-name=wlan2 ] band=5ghz-a/n/ac channel-width=20/40/80mhz-XXXX country=germany disabled=no distance=indoors frequency=auto mode=ap-bridge skip-dfs-channels=10min-cac ssid=Nebuchadnezza-5G \
    wireless-protocol=802.11 wps-mode=disabled
/interface vlan
add comment="Telekom PPPoe VLAN" interface=ether1 name=vlan7 vlan-id=7
/interface pppoe-client
add add-default-route=yes allow=pap,chap,mschap2 comment="PPPoe Telekom" disabled=no interface=vlan7 name=pppoe-telekom user=foobar
/interface list
add comment=defconf name=WAN
add comment=defconf name=LAN
/interface lte apn
set [ find default=yes ] use-peer-dns=no
/interface wireless security-profiles
set [ find default=yes ] authentication-types=wpa-psk,wpa2-psk mode=dynamic-keys supplicant-identity=MikroTik
/ip hotspot profile
set [ find default=yes ] html-directory=hotspot
/ip pool
add name=dhcp ranges=10.0.0.100-10.0.0.254
/ip dhcp-server
add address-pool=dhcp interface=bridge name=defconf
/ipv6 dhcp-server
add address-pool=pppoe-pd interface=bridge name=server-pd
/user group
add name=prometheus policy=read,test,winbox,api,!local,!telnet,!ssh,!ftp,!reboot,!write,!policy,!password,!web,!sniff,!sensitive,!romon,!rest-api
/interface bridge port
add bridge=bridge comment=defconf interface=ether1
add bridge=bridge comment=defconf interface=ether2
add bridge=bridge comment=defconf interface=ether3
add bridge=bridge comment=defconf interface=ether4
add bridge=bridge comment=defconf interface=ether5
add bridge=bridge comment=defconf interface=wlan1
add bridge=bridge comment=defconf interface=wlan2
/ip neighbor discovery-settings
set discover-interface-list=LAN
/interface list member
add comment=defconf interface=bridge list=LAN
add interface=pppoe-telekom list=WAN
/ip address
add address=10.0.0.1/24 comment=defconf interface=bridge network=10.0.0.0
/ip dhcp-server lease
add address=10.0.0.240 client-id=1:b8:27:eb:2:ff:1e comment=Pihole mac-address=B8:27:EB:02:FF:1E server=defconf
/ip dhcp-server network
add address=10.0.0.0/24 comment=defconf dns-server=10.0.0.1 gateway=10.0.0.1 netmask=24
/ip dns
set allow-remote-requests=yes use-doh-server=https://1.1.1.1/dns-query verify-doh-cert=yes
/ip dns static
add address=10.0.0.1 comment=defconf name=router.lan
/ip firewall filter
add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=input comment="defconf: drop invalid" connection-state=invalid
add action=accept chain=input comment="defconf: accept ICMP" protocol=icmp
add action=accept chain=input comment="defconf: accept to local loopback (for CAPsMAN)" dst-address=127.0.0.1
add action=drop chain=input comment="defconf: drop all not coming from LAN" in-interface-list=!LAN
add action=accept chain=forward comment="defconf: accept in ipsec policy" ipsec-policy=in,ipsec
add action=accept chain=forward comment="defconf: accept out ipsec policy" ipsec-policy=out,ipsec
add action=fasttrack-connection chain=forward comment="defconf: fasttrack" connection-state=established,related hw-offload=yes
add action=accept chain=forward comment="defconf: accept established,related, untracked" connection-state=established,related,untracked
add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid
add action=drop chain=forward comment="defconf: drop all from WAN not DSTNATed" connection-nat-state=!dstnat connection-state=new in-interface-list=WAN
/ip firewall nat
add action=masquerade chain=srcnat comment="defconf: masquerade" ipsec-policy=out,none out-interface-list=WAN
/ip service
set telnet disabled=yes
set ftp disabled=yes
set www disabled=yes
set www-ssl certificate=Webfig disabled=no
set api disabled=yes
set api-ssl certificate=Webfig
/ipv6 address
add from-pool=pppoe-pd interface=bridge
/ipv6 dhcp-client
add interface=pppoe-telekom pool-name=pppoe-pd pool-prefix-length=56 request=prefix
/ipv6 firewall address-list
add address=::/128 comment="defconf: unspecified address" list=bad_ipv6
add address=::1/128 comment="defconf: lo" list=bad_ipv6
add address=fec0::/10 comment="defconf: site-local" list=bad_ipv6
add address=::ffff:0.0.0.0/96 comment="defconf: ipv4-mapped" list=bad_ipv6
add address=::/96 comment="defconf: ipv4 compat" list=bad_ipv6
add address=100::/64 comment="defconf: discard only " list=bad_ipv6
add address=2001:db8::/32 comment="defconf: documentation" list=bad_ipv6
add address=2001:10::/28 comment="defconf: ORCHID" list=bad_ipv6
add address=3ffe::/16 comment="defconf: 6bone" list=bad_ipv6
/ipv6 firewall filter
add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=input comment="defconf: drop invalid" connection-state=invalid
add action=accept chain=input comment="defconf: accept ICMPv6" protocol=icmpv6
add action=accept chain=input comment="defconf: accept UDP traceroute" port=33434-33534 protocol=udp
add action=accept chain=input comment="defconf: accept DHCPv6-Client prefix delegation." dst-port=546 protocol=udp src-address=fe80::/10
add action=accept chain=input comment="defconf: accept IKE" dst-port=500,4500 protocol=udp
add action=accept chain=input comment="defconf: accept ipsec AH" protocol=ipsec-ah
add action=accept chain=input comment="defconf: accept ipsec ESP" protocol=ipsec-esp
add action=accept chain=input comment="defconf: accept all that matches ipsec policy" ipsec-policy=in,ipsec
add action=drop chain=input comment="defconf: drop everything else not coming from LAN" in-interface-list=!LAN
add action=accept chain=forward comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid
add action=drop chain=forward comment="defconf: drop packets with bad src ipv6" src-address-list=bad_ipv6
add action=drop chain=forward comment="defconf: drop packets with bad dst ipv6" dst-address-list=bad_ipv6
add action=drop chain=forward comment="defconf: rfc4890 drop hop-limit=1" hop-limit=equal:1 protocol=icmpv6
add action=accept chain=forward comment="defconf: accept ICMPv6" protocol=icmpv6
add action=accept chain=forward comment="defconf: accept HIP" protocol=139
add action=accept chain=forward comment="defconf: accept IKE" dst-port=500,4500 protocol=udp
add action=accept chain=forward comment="defconf: accept ipsec AH" protocol=ipsec-ah
add action=accept chain=forward comment="defconf: accept ipsec ESP" protocol=ipsec-esp
add action=accept chain=forward comment="defconf: accept all that matches ipsec policy" ipsec-policy=in,ipsec
add action=drop chain=forward comment="defconf: drop everything else not coming from LAN" in-interface-list=!LAN
/ipv6 nd
set [ find default=yes ] managed-address-configuration=yes other-configuration=yes ra-preference=low
/system clock
set time-zone-name=Europe/Berlin
/system routerboard mode-button
set enabled=yes on-event=dark-mode
/system script
add comment=defconf dont-require-permissions=no name=dark-mode owner=*sys policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon source="\r\
    \n   :if ([system leds settings get all-leds-off] = \"never\") do={\r\
    \n     /system leds settings set all-leds-off=immediate \r\
    \n   } else={\r\
    \n     /system leds settings set all-leds-off=never \r\
    \n   }\r\
    \n "
/tool mac-server
set allowed-interface-list=LAN
/tool mac-server mac-winbox
set allowed-interface-list=LAN

```

