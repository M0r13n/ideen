The following command can be used to find the largest N=20 files on Linux:

`du -a /dir/ | sort -n -r | head -n 20

- `du -a .` will print all files with their size recursively
- `sort -n -r` will sort by human readable numbers (-n) in reverse order (-r)
- `head -n 20` will print the first 20 lines