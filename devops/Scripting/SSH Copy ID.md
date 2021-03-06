# Install a SSH key on a server as an authorized key

Before you can copy your **public** key to a remote host, you need to [[fundamentals/ssh/Fundamentals|generate a SSH keypair]].

The commands follows the following pattern:

```bash
$ ssh-copy-id -i <PATH_TO_KEY> <USER>@<HOST>
```

Real world example:

```bash
$ ssh-copy-id -i ~/.ssh/id_rsa.pub pi@pi.hole
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/leon/.ssh/id_rsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
pi@pi.hole's password:


Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'pi@pi.hole'"
and check to make sure that only the key(s) you wanted were added.
```

You can log into the remote machine:

```bash
$ ssh -i ~/.ssh/id_rsa pi@pi.hole
```


## Potential errors
- Set `PubkeyAuthentication yes` in `/etc/ssh/sshd_config` on the remote
- Set `PermitRootLogin yes` in `/etc/ssh/sshd_config` on the remote
- Set `PubkeyAuthentication yes` in `/etc/ssh/config` on the remote


## What happens under the hood
```bash
$ ssh-copy-id -i ~/.ssh/id_rsa.pub pi@pi.hole
```

is equivalent to

```bash
#  Copy the public key to pi.hole
$ scp ~/.ssh/id_rsa.pub  pi@pi.hole:

# Copy the content of the public key file into the authorized keys file
$ ssh pi@pi.hole 'cat ~/id_rsa.pub >> ~/.ssh/authorized_keys'

# Delete the now unnecessary public key on the remote
$ ssh pi@pi.hole 'rm ~/id_rsa.pub'

```