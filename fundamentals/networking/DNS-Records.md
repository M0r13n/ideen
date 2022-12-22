| Record Type 	| Description |
| --- | --- |
| A Record 	| maps hostname to IPv4 address | 
| AAAA Record | A record but for IPv6 | 
| NS Record | tells the resolver about the authorative name server (next server to ask)	| 
| CNAME Record | maps a hostname to another hostname (the latter **must be resolvable** | 
| MX Record | maps mail servers to IP addesses | 
| TXT Record | any text as long as it is shorter than 255 characters |  
|  SRV Record | information about services offered by a host (e.g. port number)| 
| SOA Record (Start of Authority) 	| holds basic properties about the domain name server| 
| PTR | maps IP address to hostname (reverse A/AAAA record) | 
	| CAA Record (Certification Authority Authorization) | only this CA can issues SSL/TLS certificates for this domain (MITM protection)|
	|	ACME-CAA |  names a specific account at a specific CA (CAA + account name)|

## MitM protection

**Threat model**: Assuming that an attacker can intercept **all traffic** to a given domain regardless of where it comes from, it is trivially obtain a certificate for a website. The attacker needs to be able to intercept all traffic, because some (most) CAs make multiple **domain verification probes** from different vantage points. The idea is, that is an attacker might be able to incercept traffic coming from Berling to `leonmortenrichter.de`, but hopefully not from New York. This is true for most criminals, but is not true for global state actors. The NSA is known to be able to intcercept the traffic to whole datacenters.

**By adding a CAA record** it is possible for a domain to limit which CA can issue a certificate for it. This prevents an attacker from picking the weakest CA to issue a certificate. It is just a simple DNS record:

`leonmortenrichter.de. IN CAA 0 issue "letsencrypt.org"`

Together with DNSSEC (to prevent forgery) this limits the risk significantly. The risk can be further reduced by using an **ACME-CAA** record. This record extends the CAA record, so that is also names a specific account at a specific CA:

`leonmortenrichter.de. IN CAA 0 issue "letsencrypt.org; accounturi=https://foo.bar/some-account"`