**Samba** is an implementation of the SMB (Server Message Block)/CIFS (Common Internet File System) protocol. It can be used to share folders and printers in a network across Windows **and** Unix machines. SMB and CIFS are mostly used synonymously.

## Samba Client Configuration (Linux)

* the daemon `smbd` is offers the SMB functionality
* `smbd` offers authentication and authorization features 

### GUI (Ubuntu)
* on Ubuntu it is easy to access files from a Windows network share
* open the Nautilus file manager
* click on `+ Other locations`
* select `Networks/Windows Network`

### Manually
* Install the required package: `sudo apt install -y smbclient`
* with this tool you can:
	* list public SMB shares:
		* `smbclient -L //server -U user`
	* connect to a share:
		* `smblicnet //server/share -U user`
		* `smbclient //server/share -U user%password`

### Using CIFS
 * install the `cifs-utils` package
 * by default only **root can mount SMB shares**
	 * the cleanest way around this is to add a separate group that is allowed to mount SMB shares
```bash
# Create a new group and add N users to it
sudo groupadd samba
sudo adduser user samba # <- change user to any username

# Edit the groups permission and allow it to mount SMB shares
sudo visudo

# Add a line  in the "group" section :
## Members of the admin group may gain root privileges
%admin   ALL=(ALL) ALL
%samba   ALL=(ALL) /bin/mount,/bin/umount,/sbin/mount.cifs,/sbin/umount.cifs

```
* `%samba` can be replaced with `%users` to allow all members of the users group to mount SMB shares
* mount a network share:

```bash
# Create the folder that the share should be mounted into
mkdir /mnt/some_folder

# Mount the drive
sudo mount -t cifs //myserver_ip_address/myshare /mnt/some_folder -o username=samb_user

# Unmount:
sudo umount /mnt/some_folder

```

* the `noexec` option could prevent executable scripts from running
* the `nofail` option the OS will still boot even if the Kernel can not mount the share
* `noauto` option will prevent the Kernel from mounting the share during boot
* mount a share on boot:

```bash
# Create a file with your SMB credentials
sudo nano /etc/samba/user

# The format looks like:
username=samba_user
password=samba_user_password

# Exit nano

# Protect it (optionally)
sudo chown root:root /etc/samba/user
sudo chmod 0400 /etc/samba/user

# Edit fstab
sudo nano /etc/fstab

//myserver_ip_address/myshare  /mnt/some_folder  cifs  credentials=/etc/samba/user,noexec  0 0

# Exit and either reboot or run
sudo mount /mnt/some_folder

```
* if you omit the password from the credential file and add the `noauto` option you will be asked for the password every time you mount the share
 
## Samba Server Configuration

TBD when I actually need to set up a SAMBA share

## Samba and Active Directory

[It is possible](https://help.ubuntu.com/community/ActiveDirectoryWinbindHowto) to use Samba in an Active Directory (AD) and Kerberos environment.

## SMB protocol

The Server Message Block protocol is used to share files between clients and servers in a network. Even though it is often described as a file system it is not a file system. It it somewhat similar to NFS on Unix machines. **CIFS** is a continuation of the original **SMB** protocol maintained by Microsoft.

Although SMB/CIFS **was developed for Windows networks,** a software interface called **Samba** exists for Linux-based operating systems. Samba can be used to provide services that are typical for Windows-based networks.

### SMB and NetBIOS/NetBEUI

Before TCP/IP was a thing NetBIOS and NetBEUI were used as transport layer protocols. But they are mostly outdated today.

## SMB communication

- just like [[HTTP]] SMB is a client-server protocol
	- request/response model
	- the client requests some resource from a server
	- the communication is **always initiated** by the client
* since SMB3 the protocol supports multiple connection per session (multichannel)


## Ressources

- https://help.ubuntu.com/community/Samba
- https://www.elektronik-kompendium.de/sites/net/2101131.htm