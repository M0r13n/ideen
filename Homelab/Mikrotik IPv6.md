# Mikrotik IPv6 with PPPoe

```
/ipv6 dhcp-client
add interface=pppoe-out1 pool-name=pppoe-pd pool-prefix-length=56 request=prefix
/ipv6 dhcp-server
add interface=bridge address-pool=pppoe-pd name=server-pd
/ipv6 address
add interface=bridge from-pool=pppoe-pd advertise=yes
```