| dir | user | group | other |
| --- | ---  | ---   | ---   |
|  **d**   | **r \| w \| x** | **r \| w \| x**  | **r \| w \| x**  |
| |4 \| 2 \| 1 | 4 \| 2 \| 1| 4 \| 2 \| 1|


- view permissions of files with `ls -la`
	- the result will list he permissions ten char code: **drwxrwxr-x**
		- r = readable
		- w = writable/deletable
		- x = executable
		- for each group in the order: **user, group** and **others**
	- often times these permissions are expressed numerical (octal)
	- the permissions are added and shown as a single number
		- 0 = no permissions
		- 1 = executable
		- 2 = writable
		- 4 = readable
		- thus 640 means:
			- 4 + 2 = writable + readable by the owner
			- 4 = readable by the owning group
			- 0 = others have no permissions
- permissions are modified using `chmod`:
	- `chmod 755 filename`
	- `chmod u=rwx,go=rx filename`
	- permissions can be added `chmod u+x filename`
	- or removed `chmod o-r filename`