# Read-Only Filesystems

## Why

- prevent any changes from occuring to the root filesystem
- allow a simple reboot to restore the system to its pristine state
- limit writes to the disk to prolong the lifetime of disks

## What to consider?

- how to adjust the configuration using files afterwards?
- what happens to the systemclock after a reboot?
- where to place the driftfile?
- what appens with daily `apt` tasks?
- how to update/patch the system?
- where to store logs?
- where to place `/var/lib/sudo`?
- what about [`systemd-random-seed`](https://www.freedesktop.org/software/systemd/man/latest/systemd-random-seed.service.html)
- logging services create logfiles
- services create temporary config files
- some services need a cache they can write to

## [OverlayFS](http://en.wikipedia.org/wiki/OverlayFS)

OverlayFS can do exactly that: by layering several file systems one can show data from one (the 'lower') filesystem, but have all changes to the data end up in a different (the 'upper') file system. If the lower filesystem is our SD card and the upper filesystem is a temporary filesystem in RAM, we have effectively separated our SD card from all write-attempts of the operating system. Without the operating system even noticing.

OverlayFS presents a unified view of two different filesystems; the presented filesystem is the result of overlaying one filesystem over another. There are two filesystems:

1. **upper filesystem:** read-write mount of some block device (e.g. `tmpfs`)
2. **lower filesystem:** read-only mount of the root filesystem

If a node exists in both filesystems the node from the *upper* filesystem is presented - the *lower* node is hidden. Directories are merged before they are presented.

Any change made on top the root filesystem is stored on the *upper* filesystem. Depending on the block device chosen, these changes can be temporary (`tmpfs`) or permanent.

- OverlayFS is commonly used in scenarios where a read-only base filesystem needs to be combined with a writable layer for temporary changes or modifications.
- It is suitable for scenarios where runtime modifications are necessary but need to be isolated from the underlying read-only filesystem.

### Example

- `/dev/sda1` is mounted as `/`
- `/dev/sda2` is mounted as `/data`

By mounting `/` using overlayroot with an *upper* filesystem using `tmpfs` changes won't be persisted on `/`. In order for applications to persist data, they have to write to `/data`.

## [SquashFS](https://en.wikipedia.org/wiki/SquashFS)

SquashFS is optimized for high data density and compression, and already well established. OverlayFS and UnionFS are suitable for scenarios requiring runtime modifications and dynamic filesystem management, while SquashFS excels in space efficiency and read-only access.
