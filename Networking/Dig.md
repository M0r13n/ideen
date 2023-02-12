
```bash
# Get only the address
dig leonmortenrichter.de A +noall +answer

# Get a list of nameservers
dig leonmortenrichter.de +noall +answer

# Get an IPv6 record
dig leonmortenrichter.de AAAA +noall +answer

# Reverse lookup using a PTR
dig -x 10.0.10.209 +short

# TXT records
dig leonmortenrichter.de TXT +short

# Trace the resolution
dig leonmortenrichter.de +trace +short

```