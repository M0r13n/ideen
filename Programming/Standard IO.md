- use the pipe to redirect output into other programs
	- `echo "foo" | grep "foo"`
- use > to redirect output to different file descriptors
	- `ls / > output_file.txt`
- use `2>&1` to merge stderr and stdout together to stdout
	- it must **follow a file redirection**
	- it must **precede a pipe redirection**
- stdout is buffered
- stderr is not buffered