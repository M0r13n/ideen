# The Linux Directory Structure

You may refer to the [Filesystem Hierarchy Standard](https://www.pathname.com/fhs/pub/fhs-2.3.html)


- `/` Root Directory
	- everthing is stored under `/`
	- includes **all** partitions (e.g. `/mnt/drive`)

- `/bin` important user binaries
	-  all required executables that have to be present in single-user mode
	-  `single-user mode`: the system boots with your local file systems mounted, many important services running, and a usable maintenance shell that allows you to perform many of the usual system commands. no other filesystems are mounted.
	- [Required programs](https://www.pathname.com/fhs/pub/fhs-2.3.html#REQUIREMENTS2)
	-  `/sbin` is a special location for system administration binaries
	
- `/boot` Static files required during boot
	- everthing that is needed to boot the system is store here

- `/dev` Device files
	- **In Linux everything is a file**
	- inside `/dev` there are special files for devices
   - Device files usually provide simple interfaces to standard devices (such as printers and serial ports), but can also be used to access specific unique resources on those devices, such as [disk partitions](https://en.wikipedia.org/wiki/Disk_partitioning).
   - may also contained pseudo-device files (`dev/urandom`)

- `/etc` configuration files
	- mostly plain text files that can be edited with a text editor
	- `/etc` -> system wide configuration files
	- `$HOME/etc` -> user specific config files

- `/mnt` Temporary Mount Points
	- everthing is stored under `/`
	- mostly used for things mounted manually
	- the system most likely mounts under `/media`

- `/opt` Add-on application software packages
	- everthing is stored under `/`
	- place for applications that are not installed by a package manager or that come with a proprietary licence
	- programs are installed under `/opt/<package>` or `/opt/<package>` (e.g. `/opt/jfrog/artifactory`)

- `/srv` Data for services provided by this system
	- readonly data, writable data and scripts
	- used for site-specific data which is served by this system
	- not fully specified (layout is application specific)

- `/tmp` Temprary files
	- Programs must not assume that any files or directories in `/tmp` are preserved between invocations of the program.

- `/usr` Root Directory
	- shareable, read-only data
	- must be shareable between various FHS-compliant hosts and must not be written to
	- stores most system tools, libraries, installed program
	- the name is historical - in the past, when /home did not exist, the user directories were also located here
	- `/usr/bin` Most user commands
	- `/usr/include` Header files included by C programs
	- `/usr/lib` Libraries
	- `/usr/local` Local hierarchy (empty after main installation)
	- `/usr/sbin` Non-vital system binaries


- `/var` Variable data files
	- includes spool directories and files, administrative and logging data, and transient and temporary files.
	- `/var/log` system wide log files
	- `/var/run` Files that store the state of the entire system; contents are deleted and rewritten aduring boot
	- `/var/tmp` files that need to be persisted between reboots
	- `/var/www` document roots of the web server Apache

- `/proc` Kernel and process information virtual filesystem
	-  Good advice: Do not touch ;-)
