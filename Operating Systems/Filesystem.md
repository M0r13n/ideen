# File System Interface

- a *file* is a named collection of related information that is recorded on secondary storage
- *files* are organised in a *directory structure* which organises and provides information about all files on the system
- the operating system provides a uniform logical view of stored information
- the physical storage devices are abstracted into logical storage units

## Attributes

- **Name.** A human-readable name only used for better usability.
- **Identifier.** A unique number (Inode) identifying the file within the file system.
- **Type.** On UNIX this is either regular file or executable.
- **Location.** Pointer to a device and the location of the file on that device.
- **Size.** Current size of the file in bytes and blocks.
- **Protection.** Access-Control information (read, write,exec).
- **Metadata.** Timestamps and Owner information.

## Operations

UNIX requires that the programmer explicitly opens a file using the `open()` system call before using it. This system call takes a file name as well as access mode information. `open()` then returns a pointer to the entry of the file in the **open-file table** - a system wide table containing information about all open files (for better performance). The **per-process table** tracks all files that a process has open. For instance, it stores the current file pointer as well as access rights. Each entry in this table points to a entry in the system wide file table, which holds information that is process independent: inode, location on disk, access dates, size. It also contains a `open count` that counts how many processes opened the file/