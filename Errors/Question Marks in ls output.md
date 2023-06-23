`ls` does not report correct permissions and is just showing question marks:

```bash
leon at leon-tux in ~/projects/ideen on main [!?]
$ ls -l
d????????? ? ? ? ?   - leon 31 Dec  2022 /some/folder
```

- most likely caused by failing `stat()` syscall
- missing execution permission on a directory may cause this (see [[File Permissions#Directories]])
- improperly mounted file systems also cause this
  - the mount point of that filesystem may show up with question marks
  - thinclient_drives when using xrdp