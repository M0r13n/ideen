# Uncomplicated Firewall (UFW)

[ufw](https://launchpad.net/ufw) is a terminal application that serves as a frontend for iptables. There is a **unofficial** graphical interface for ufw: gufw

## Important
By default ufw blocks **all incoming** connections unless explicitly  configured otherwise. In case you are accessing a remote machine through [[Security/SSH]] you might block yourself from the system. In this case physical access to the machine is **mandatory**. Therefore, make sure to always configure ufw properly **before** enabling it.

## Installation and basic configuration

The following configuration can be safely used for all of my systems.

```bash
# Install ufw
sudo apt install ufw -y

# Check the status of ufw [default: inactive]
sudo ufw status

# Allow all outgoing connections, block incoming connections
sudo ufw default allow outgoing
sudo ufw default deny incoming

# Enable IPv6 support
grep -i 'ipv6=yes'  /etc/default/ufw >/dev/null && echo IPv6 enabled || echo IPv6 disabled

# Allow SSH with rate limiting
sudo ufw allow ssh
sudo ufw limit ssh

# sudo ufw allow 2222/tcp

sudo ufw enable
sudo ufw status
```

## Handy commands

`sudo ufw allow|deny [proto <PROTOCOL>] [from <FROM_ADDRESS> [port <PORT>]] [to <TO_ADDRESS> [port <PORT>]] [comment <COMMENT>]`

Allow connections to a specific port:

`sudo ufw allow 80/tcp comment 'accept webtraffic'`

Allow connections to a range of ports:

`sudo ufw allow 3000:4000/udp`

Allow **ALL** connections from a given **remote IP**:

`sudo ufw allow from  123.123.123.123`

Allow connections to SSH from a specific IP:

`sudo ufw allow from 123.123.123.123 to any port 25 proto tcp`

Deny connections from a given IP or subnet:

`sudo ufw deny from  123.123.123.123`
`sudo ufw deny from  123.123.123.123/32`

Delete a rule

```bash
sudo ufw status numbered
sudo ufw delete 6
```

Reset **all** rules

`sudo ufw reset`

Apply changes

`sudo ufw reload`

Retrieve logs

```bash
# Logging needs to be turned on explicitly
sudo ufw logging on
sudo more /var/log/ufw.log
sudo tail -f /var/log/ufw.log
```

List rules

```bash
sudo ufw show listening
sudo ufw show added
```

## Details

### Configuration

ufw uses the following configuration files in the following order:

1.  **/etc/ufw/before.rules**
2.  **/var/lib/ufw/user.rules**
3.  **/etc/ufw/after.rules**

with 1<2<3

### deny vs reject

Both `deny` and `reject` block network traffic for a given service. But in case of `reject` the sender gets a notification, that its attempt got rejected.

### any

The parameters `PROTOCOL`, `ADDRESS` and `PORT` can be substituted with `any`. `any` is always true.


## Playbook

This playbook uses [[Ansible]].

```yaml
---

- name: Enable ufw
  ufw: state=enabled policy=allow

- name: Disable default in
  ufw: direction=incoming policy=deny

- name: Allow ssh in
  ufw: rule=limit name=OpenSSH

# - name: 80 is open
#   ufw: rule=allow port=80 proto=tcp

# - name: 4949 (munin-node) is open to monitor(s)
#   when: install_muninnode|default(True)
#   ufw: rule=allow port=4949 proto=tcp from_ip={{ item }}
#   with_items: "{{ muninnode_query_ips|default([]) }}"
```