- [docs](https://gitlab.com/apparmor/apparmor/-/wikis/Documentation)
- mandatory access control for individual programs
- define policies for files, capabilities or network access
- selective confinement: every program is treated individually
- use the **learning mode** to learn a programs behavior which can then be **enforced**
- check if the current distribution has AppArmor enabled:
```bash
$ aa-status    
apparmor module is loaded.
```
- relevant files can be found under  `/etc/apparmor.d`
	- profiles for snaps are found here: `/var/lib/snapd/apparmor/profiles/`
- `aa-autodep` guess basic profile requirements
- logs can be viewed with `journalctl -fx`:
	- `--follow --catalog`
	- or use `dmesg`
- useful package on debian is `apparmor-utils`:
	- `aa-complain`
	- `aa-status`
	- `aa-enforce`
	- ...
- profiles are based on **default deny**
	- <mark>the profile list what is allowed and everything else is denied</mark>
	- explicit denials are possible but only to document known bad behaviors


## Docker

- comes with the default profile `docker-default`
- `apparmor_status` should list the docker-default profile as enforced
- `sudo aa-status` should report each container process in enforce mode
	- `/usr/bin/busybox (19731) docker-default`


## Raspi

- starting with v5.10 of the Linux Kernel AppArmor is  supported by Raspian
- to enable add `lsm=apparmor`  to `/boot/cmdline.txt`

## Python

- possible to run interpreted programs/languages
- requires a nested profile
```txt
#include <tunables/global>

profile /home/leon/projects/foo/foo flags=(attach_disconnected,mediate_deleted) {
    #include <abstractions/base>
    #include <abstractions/python>

    /usr/bin/python3.10 ix,
    @{HOME}/projects/foo/** r,
}
```