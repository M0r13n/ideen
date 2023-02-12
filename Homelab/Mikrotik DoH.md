# Configure DNS over HTTPS with Mikrotik
```bash
# Temporarily add a normal upstream DNS resolver
/ip dns set servers=1.1.1.1,1.0.0.1

# CA certificates extracted from Mozilla
/tool fetch url=https://curl.se/ca/cacert.pem

# Import the downloaded ca-store (127 certificates)
/certificate import file-name=cacert.pem passphrase=""

# Set the DoH resolver to cloudflare
/ip dns set use-doh-server=https://1.1.1.1/dns-query verify-doh-cert=yes

# Remove the old upstream DNS resolvers
/ip dns set servers=""

# Delete the certificate file
/file remove cacert.pem

# OPTIONAL - Disable DDNS
/ip dhcp-client set use-peer-dns=no # Enter 0 as a number if it asks you

# If you are connection over LTE (for exmaple with a chateau)
/interface lte apn set use-peer-dns=no # Enter 0 as a number if it asks you

# Verify, that DynDNS is disabled
/ip dns print
```