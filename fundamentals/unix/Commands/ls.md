# Linux command `ls`

- list the contents of a directory



#### List contents of dir
```bash
ls /home/leon
bin code dotfiles Downloads go irc logs src
```

#### Include hidden files and folders
```bash
ls -a /home/george
.aliases       .bash_prompt  .dockerfunc  .gitkeep     .nanorc    ...
```

#### Include files types
```bash
ls -F
```
- `/` indicates a directory
- `@` indicates a symbolic link
- `|` indicates a FIFO
- `=` indicates a socket
- `>` indicates a door
- nothing is shown for regular files

#### Long listing
```bash
ls -l
drwxr-xr-x - leon 24 May 15:29 dotfiles
```

| Field Index | Example          | Description                                                                                     |
|-------------|------------------|-------------------------------------------------------------------------------------------------|
| 1           | **d**            | file type(**-**: file, **d**: dir, **l**:link)                                                  |
| 2-4         | **rwx r-x r-x**  | Permission: (read, write, execute) 1: owner, 2: group, 3: everybody (extended permissions: `+`) |
| 5           | **-**            | Number of hard links (created through `ln` **without** `-s`                                     |
| 6           | **leon**         | Owner name                                                                                      |
| 7           | **24**           | Owner group as name or gid                                                                      |
| 8           | **2048**         | File size in bytes                                                                              |
| 9           | **Jan 21 07:11** | Last modified                                                                                   |
| 10          | **some_file**    | File or directory name                                                                          |
|             |                  |                                                                                                 |
|             |                  |                                                                                                 |
|             |                  |                                                                                                 |



#### Useful options
- sort by size: `-S`
- sort by modification time: `-t`
- sort by access time: `-u`
- display file size in a human readable format: `-h`
- recursive listing: `-R` (better use `tree`)