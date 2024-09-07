# Checkmk

Create a new site:

```bash
# Create the site
sudo omd create <sitename>

# Copy all rule files (assuming they exist)
cp *.mk /omd/sites/<sitename>/etc/check_mk/conf.d/wato/

# Fix their permissions
sudo chown <sitename>:<sitename> /omd/sites/<sitename>/etc/check_mk/conf.d/wato/*.mk

# Reload
sudo su - <sitename> -C 'cmk -I'
sudo su - <sitename> -C 'cmk -O'

# Set password
sudo su - <sitename> -C 'cmk-passwd'

# Start site
sudo omd start <sitename>
```

## Nvidia-smi

Create an **executable** file in `/usr/lib/check_mk_agent/plugins/` (on the agent/client):

```bash
#!/bin/bash
echo "<<<nvidia_smi:sep(9)>>>"
nvidia-smi -q -x
```
