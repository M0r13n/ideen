# Helpful commands that I always forget about

| Command 	|  Description  |  Exmaple  |
|-----------|---------------|-----------|
| install   | install program copies files (often just compiled) into destination locations you choose,, while setting permission modes and owner/group. |   `install ./some_program ~/bin/some_program`|
| fc        | used to list or edit and re-execute commands from the history list. FIRST and LAST can be numbers specifying the range, or FIRST can be a string, which means the most recent command beginning with that string. | `fc 1234` |
| blkid | command-line utility to locate/print block device attributes. Very useful for getting the UUID of a drive for fstab. | `blkid -t TYPE=ntfs ` or `blkid -o list ` |
