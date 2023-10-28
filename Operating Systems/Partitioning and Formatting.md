# Partitioning and Formatting

General overview of ways to partition drives and formatting them using common file systems.

## LVM logical volume on traditional partition

Sometimes a logical volume is mapped to a traditional partition:

```bash
root@agw:~# lsblk /dev/vda
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
vda                  252:0    0   20G  0 disk 
├─vda1               252:1    0    1M  0 part 
├─vda2               252:2    0  513M  0 part /boot/efi
└─vda3               252:3    0 19.5G  0 part 
  ├─vgxubuntu-root   253:0    0 18.5G  0 lvm  /
  └─vgxubuntu-swap_1 253:1    0  976M  0 lvm  [SWAP]
```

In this case it does not suffice to just grow the LVM, because the underlying partition is itself limited in size. Thus, the traditional partition has to be grown using `growpart` first:

`sudo growpart /dev/vda 3`



Afterwards, the LVM can be grown the regular way:

1. lvextend: `lvextend -l+100%FREE /dev/vgxubuntu/root`
2. resize2fs: ` resize2fs /dev/mapper/vgxubuntu-root`