# Foo Server

The appication servers (or app servers) are the Apache servers that serve the content.

## Service

Ansible roles.playbooks:

- `company.xzy.app-server`
- `company.xzy.sso`

## Authentication

You can authenticate as `root` with an SSH key signed by [Fancy CA]().

## Connections

| Source | Source Port(s) | Destination       | Destination Port(s) | Comment/Description     |
|--------|----------------|-------------------|---------------------|-------------------------|
| `foo`  | n.a.           | `bar`             | 443                 | Fetch data              |
| `foo`  | n.a.           | archive.ubuntu.de | 80, 443             | Fetch updates via `apt` |


## Configuration

The `/etc/sshd/sshd_config` should look like this:

```conf
# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# Authentication:

#LoginGraceTime 2m
#BC# Root only allowed to login from LAN IP ranges listed at end
#PermitRootLogin no
PermitRootLogin yes
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

#RSAAuthentication yes
#PubkeyAuthentication yes
#AuthorizedKeysFile  .ssh/authorized_keys

# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#RhostsRSAAuthentication no
# similar for protocol version 2
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# RhostsRSAAuthentication and HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
#BC# Disable password authentication by default (except for LAN IP ranges listed later)
PasswordAuthentication no
PermitEmptyPasswords no
#BC# Have to allow root here because AllowUsers not allowed in Match block.  It will not work though because of PermitRootLogin.
#BC# This is no longer true as of 6.1.  AllowUsers is now allowed in a Match block.
AllowUsers kmk root

# Change to no to disable s/key passwords
#BC# I occasionally use s/key one time passwords generated by a phone app
ChallengeResponseAuthentication yes

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
X11Forwarding yes
#X11DisplayOffset 10
#X11UseLocalhost yes
#PrintMotd yes
#PrintLastLog yes
#TCPKeepAlive yes
#UseLogin no
#UsePrivilegeSeparation yes
#PermitUserEnvironment no
#Compression delayed
#ClientAliveInterval 0
#ClientAliveCountMax 3
#UseDNS yes
#PidFile /var/run/sshd.pid
#MaxStartups 10
#PermitTunnel no
#ChrootDirectory none

# no default banner path
#Banner none

# override default of no subsystems
#Subsystem	sftp	/usr/lib/misc/sftp-server
Subsystem	sftp	internal-sftp

#BC# My internal networks
#BC# Root can log in from here but only with a key and kmk can log in here with a password.
Match Address 172.22.100.0/24,172.22.5.0/24,127.0.0.1
  PermitRootLogin without-password
  PasswordAuthentication yes
```

## Backup

The server is backuped by `restic`.

To get started, first define some environment variables:

```bash
export RESTIC_REPOSITORY=/srv/restic-repo
export RESTIC_PASSWORD=some-strong-password
```

Initialize the repository (first time only):

`restic init`

Create your first backup:

`restic backup ~/work`

You can list all the snapshots you created with:

`restic snapshots`

You can restore a backup by noting the snapshot ID you want and running:

`restic restore --target /tmp/restore-work your-snapshot-ID`

It is a good idea to periodically check your repository’s metadata:

`restic check`

or full data:

`restic check --read-data`
