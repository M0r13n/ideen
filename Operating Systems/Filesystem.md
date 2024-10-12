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

## File Types

- **File extension:** most common way to determine a file's type
- **Magic numbers:** unique "magic number" or "file signature" at the beginning of the file.This is a sequence of bytes that identifies the file format.

Linux systems use MIME type databases to map file extensions and magic numbers to MIME types. The most common database is the mime.types file, usually located at `/etc/mime.types` or `/usr/share/mime/mime.types`. This file contains a list of MIME types, their corresponding file extensions.

```py
# https://en.wikipedia.org/wiki/List_of_file_signatures

# Create a Amiga Hunk executable file
with open('/tmp/foo.bar', 'wb') as fd:
    fd.write(b"\x00\x00\x03\xF3")
    fd.write(bytes(128))

# $ file foo.bar
# foo.bar: AmigaOS loadseg()ble executable/binary

# Create a file with a #!
with open('/tmp/foo.bar', 'wb') as fd:
    fd.write(b"\x23\x21")  # -> shebang #!
```

## Directory Structure

- symbol table that maps names to control blocks
- implemented as a **tree**
  - single root directory
  - any number of subdirectories (nodes)
  - files are leaves
- directories are implemented as special files -> `IS_FILE: bool`
- each node in the directory tree has:
  - name
  - type
  - Inode:
    - file type
    - ownership
    - permissions
    - timestamps
    - file size
    - block pointers
  - single parent node
  - multiple children
- the Inode is a reference to the Inode in the Inode table
  - `ls -i` shows the Inode number
- acyclic graphs allow for file sharing:
  - **hard link**: directory entry with the same Inode
  - **soft link:** soft links Inode contains a path to the referenced file
- the Inode is only deleted if all linking hard links are also removed (reference counting)
- soft links are left when a file is deleted
  - it is up to the user to handle this

## Filesystem Protection

- goal: prevent physical damage & improper access
- `rwx` <=> Read, Write, Execute
- **Access Control List (ACL)** identity based access per file/directory
	- owner, group, other
	- precedence based on granularity
		- the more specific the specification, i.e. the more precise the path, the higher the precedence
- 9 bits per file to access the access on Linux

| Owner | Group | Other |
|-------|-------|-------|
| `rwx` | `r-x` | `r--` |
| `111` | `101` | `100` |
| `7`   | `5`   | `4`   |

## Ext4 Casefold

Newer version of the Linux Kernel support the `casefold` Feature of ext4. This enables case-insensitive directories.

```bash
# Enable the feature
tune2fs -O casefold /dev/sdX1
# Verify
tune2fs -l /dev/sdX1 | grep -i casefold
# Enable the casefold feature on a per directory basis
chattr +F /mnt/directory_name
```
