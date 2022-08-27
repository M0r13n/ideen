# IPv6

## Dual Stack

Modern operating systems support that a host has an IPv4 and IPv6 address simultaneously. This is used to make the transition from IPv4 to IPv6 easier, because services can be migrated one after another. The only downside is the added complexity. Some things need to be configured twice (routing, firewalls, etc.).

### Address Selection

- a host has both: a global IPv4 and a global IPv6 address
- the host chooses the type of connection for **each new outgoing connection**
- RFC6723 says that IPv6 is preferred over IPv4
- sometimes hosts deviate from this and prefer the faster connection
