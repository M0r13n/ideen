# Cheatsheet for nssdb and certutil

- [NSS shared DB](https://wiki.mozilla.org/NSS_Shared_DB_And_LINUX) is SQLite database found in:
  - `~/.pki/*nssdb*` (user)
  - `/etc/pki/nssdb` (systemwide)
  - systemwide folder is often ignored (by chromium at least)
- remove database: `rm -r ~/.pki/nssdb`
- `certutil` is part of **libnss3-tools** on Ubuntu
- list certificates: `certutil -d sql:$HOME/.pki/nssdb -L`
- show details: `certutil -d sql:$HOME/.pki/nssdb -L -n <certificate nickname>`
- insert cert: `certutil -d sql:$HOME/.pki/nssdb -A -t <TRUSTARGS> -n <certificate nickname> -i <certificate filename>`
  - for a root cert: `certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n <certificate nickname> -i <certificate filename>`
  - intermediate cert: `certutil -d sql:$HOME/.pki/nssdb -A -t ",," -n <certificate nickname> -i <certificate filename>`
  - server certificate: `certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n <certificate nickname> -i <certificate filename>`
- delete cert: `certutil -d sql:$HOME/.pki/nssdb -D -n <certificate nickname>`
