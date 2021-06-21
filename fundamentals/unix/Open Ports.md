# TCP and UDP ports

- In linux everything is a file
- so also ports are [[file descriptors]]
- a port is a 16 bit integer (0 - 65535)
- reserved: **0** trough **1023**
- registered: **1024** **49151**
- dynamic/private: **49152+**


## List open ports on current machine

- Linux stores open ports in a file called `/etc/services`
- `tail /etc/services`

```
vboxd           20012/udp
binkp           24554/tcp                       # binkp fidonet protocol
asp             27374/tcp                       # Address Search Protocol
asp             27374/udp
csync2          30865/tcp                       # cluster synchronization tool
dircproxy       57000/tcp                       # Detachable IRC Proxy
tfido           60177/tcp                       # fidonet EMSI over telnet
fido            60179/tcp                       # fidonet EMSI over TCP
```


### `lsof`

```
**\# lsof**

COMMAND    PID      USER   FD      TYPE     DEVICE  SIZE/OFF       NODE NAME
init         1      root  **cwd**      **DIR**      253,0      4096          2 /
init         1      root  **rtd**      **DIR**      253,0      4096          2 /
init         1      root  **txt**      **REG**      253,0    145180     147164 /sbin/init
init         1      root  **mem**      **REG**      253,0   1889704     190149 /lib/libc-2.12.so
init         1      root   0u      **CHR**        1,3       0t0       3764 /dev/null
...
```


- **FD** - file descriptor:
	- **cwd**: current working dir
	- **rtd**: root dir
	- **txt**: txt program text
	- **mem**: memory mapped file
	
	- Access levels: **r**: read, **w**: write, **u**: read/write 

- **TYPE**
	- **dir** - directory
	- **reg** - regular file
	- **chr** - character
	- **fifo** - Firs In First Out queue
	
	
### List open files for user
```bash
$ lsof -u leon

#=> -u : specify username
```

### Find process running on port
```bash
$ lsof -i TCP:22

#=> -i : list only ipv4 / ipv6 network files
#=> TCP:22 : optional filter
#=> TCP:1-1024 would also be possible
```

### List open files in port range
```bash
$ lsof -i :1-1024 
$ lsof -i TCP:1-1024 
$ lsof -i :8080
```


### Search open files by PID
```bash
$ lsof -p 1
# or
$ lsof -p 1 -i
```



## Check open ports on remote

- you could use nmap
- but it is not always installed
- simple alternative is **netcat**: `nc`


```bash

# Synopsis: nc [options] [host] [port/port-range]


# Without -v flag nc returns 0 if a > 1 port is open and 1 otherwise
$ nc -z pi.hole 20-80

# List verbose messages
$ nc -z pi.hole 20-80 -v 

# -w1 specificies timeout
$ nc -zw1 pi.hole 20-80 -v

```