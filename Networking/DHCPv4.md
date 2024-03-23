
## Search Domain

- optional domain suffix
- used in conjunction with DHCP
- mechanism to convert a machine name to a FQDN
- basically a list of domains that the DNS resolver will append to a hostname when attempting to resolve it to an IP address

## DHCP Identifier

_Sets the source of DHCP (v4) client identifier. If mac is specified, the MAC address of the link is used. If this option is omitted, or if duid is specified, networkd will generate an RFC4361-compliant client identifier for the interface by combining the link’s IAID and DUID. (netplan)_


[RFC4361](https://www.rfc-editor.org/rfc/rfc4361#section-6.1):

```txt
Code  Len  Type  IAID                DUID
+----+----+-----+----+----+----+----+----+----+---
| 61 | n  | 255 | i1 | i2 | i3 | i4 | d1 | d2 |...
+----+----+-----+----+----+----+----+----+----+---
```

```txt
DHCPv4 Client ID = ff:5d:e2:6c:15:0:2:0:0:ab:11:f9:f9:80:f7:f7:20:2c:f5
                  |--|-----------|-------------------------------------|
  Client ID type = ff                                     (255 = DHCPv6 IAID+DUID)
     DHCPv6 IAID =    5d:e2:6c:15                           (siphash of "enp2s0"?)
     DHCPv6 DUID =                0:2:0:0:ab:11:f9:f9:80:f7:f7:20:2c:f5
                                 |---|---------|-----------------------|
DHCPv6 DUID type =                0:2                                (2 = DUID-EN)
  DUID-EN vendor =                    0:0:ab:11                  (43793 = systemd)
    DUID-EN data =                              f9:f9:80:f7:f7:20:2c:f5
```

Relevant files:

- `/etc/machine-id`
- `/etc/netplan/*`
- `/etc/dhcp/dhclient.conf`

