# Basic Hardening of Mikrotik devices
These are the steps that I consider reasonable for a home(lab) environment in terms of security. There are more advanced security features available and it is possible to limit/restrict even more services (don't allow HTTPS access, etc.). But these are 
exaggerated for personal setup in my humble opinion. But this depends on your threat model.

#### Only allow access from the internal network

`user set [find] address=192.168.0.0/24`

#### Deactivate unused services
`ip service disable telnet,ftp`

#### Only allow access to these services from local net
`ip service set [find] address=192.168.0.0/24`

#### Disable the bandwidth server
`tool bandwidth-server set enabled=no`

#### Disable UPnP
`ip upnp set enabled=no`

#### Disable DynDNS
`ip cloud set ddns-enabled=no`

#### Force strong crypto
`ip ssh set strong-crypto=yes`

#### Enable HTTPS
It might be sensible to disable HTTP(S) access completely. But at least SSL should be set up.
```bash
certificate add name=LocalCA common-name=LocalCA key-usage=key-cert-sign,crl-sign
certificate sign LocalCA
certificate add name=Webfig common-name=192.168.0.1
certificate sign Webfig ca=LocalCA
ip service set www-ssl certificate=Webfig disabled=no
ip service set www disabled=yes
ip service set api-ssl certificate=Webfig disabled=no
```