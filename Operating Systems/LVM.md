LVM stands for Logical Volume Manager. It is used to dynamically manage partitions across multiple physical drives. Therefore, is serves as an additional logical layer between the partition table and the file system.

### Advantages

- highly flexible
- volumes can be created, extended and reduced  dynamically (while the system is running)
- use any number of disks as one big disk.    
- snapshots can be used to created frozen copies of the file system    

### Disadvantages
- more complicated
- requires multiple background daemons

### Terminology

**Physical volume (PV)**
Unix block device node, usable for storage by LVM. Examples: a hard disk, an [MBR](https://wiki.archlinux.org/title/MBR "MBR") or [GPT](https://wiki.archlinux.org/title/GPT "GPT") partition, a [[Loopback file]], a device mapper device (e.g. [dm-crypt](https://wiki.archlinux.org/title/Dm-crypt "Dm-crypt")). It hosts an LVM header.

**Physical extent (PE)**
The smallest contiguous extent (default 4 MiB) in the PV that can be assigned to a LV. Think of PEs as parts of PVs that can be allocated to any LV. Similar to sectors in traditional hard drives.

**Volume group (VG)**
Group of PVs that serves as a container for LVs. PEs are allocated from a VG for a LV.

**Logical volume (LV)**
"Virtual/logical partition" that resides in a VG and is composed of PEs. LVs are Unix block devices analogous to physical partitions, e.g. they can be directly formatted with a [file system](https://wiki.archlinux.org/title/File_system "File system"). Works like a regular partition. Comes with a file system and can be (un)mounted.

### Cheatsheet

- expand volume to 100%: `lvextend -l +100%FREE`