# How do Pipes actually work
Pipes are a fundamental part of every Unix based OS. They allow you to pass output between processes and therefore allow you to chain multiple commands (processes) together.

Anybody who has ever worked with some kind of Unix system will know about these kinds of commands:

`ls -a | sort | more`

This command lists the contents of the current working directory, sorts it and then passes it to `more`. The latter paginates the output, so that it fits into a single terminal window.

## Implementation details
What is a `pipe`?


### It behaves like a file
A pipe behaves just like a normal Unix file. You can write and read to it. Unlike normal files pipes are mounted in a special file system. Every Linux system has such a `VFS` (*virtual file system*), that is mounted alongside `/` (your root file system). You as a user can not directly interact with it, because it is managed by the Kernel. This also means that you can not examine it. There is no way to do: `ls pipe:/`. 

### It is a fixed sized FIFO queue
A pipe is a fixed sized FIFO (First-In-First-Out Queue) that reside in memory. On my system (`Ubuntu 20.04`) a pipe has a default capacity of  `65,536` bytes. This means that the first thing that you through at it, it the same thing that comes out at the other end of the pipe. 

Pipes have some caveats:

If process `A` wants to read from a empty pipe, the `read()` syscall will block until data is available. This means that `A` is blocked until `B` writes to the pipe or closes it's [[File Descriptors]] pointing to the pipe. The latter will return `EOF`. Otherwise `A` starts reading immediately as soon as `B` starts writing.

If a pipe is full it will also block. 

## Unnamed pipes
Typically you will use the `|` character to connect `N` processes. 

Example: `ls | sort`

1. Two child processes will be created: `ls` and `sort`
2. A unnamed pipe (`P`) will be created by the Kernel
3. `ls` will write it's `stdout` to `P` (overwrite the `stdout` file descriptor)
4. `sort` will read from the other end of the pipe (overwrite the `stdin` file descriptor)
5. The Kernel schedules `ls` and `sort` to run in parallel
6. `ls` starts writing to the pipe
7. `sort` starts reading from the pipe
8. They do their work in parallel (`sort` does not have to wait for `ls` to finish it's work)
9. When `ls` finishes, it closes all of it's file descriptors
10. `sort` reads `EOF` and stops as well
11. The Kernel will remove all resources associated with the pipe

## Named pipes
Pipes behave like files and can also be used like files. 

`mkfifo /tmp/test_pipe`

As the name of `mkfifo` suggests it creates a FIFO queue named `test_pipe` in the `/tmp` directory. 

```sh
$ ls -l test_pipe
prw-r--r-- 1 leon leon 0 Jan 31 11:37 test_pipe
```

Notice the properties of the pipe:

- `prw-r--r--`: the letter `p` indicates that it is a pipe
-`1` : there exists a single file descriptor pointing to it
- `leon leon`: it is owned by my current user
-`0`: it has a size of `0` bytes


Now we can write to the pipe just as we can with any other file:

`ls -l > /tmp/test_pipe`

This programs hangs, because the other side needs to open the pipe first.

```
$ cat ./test_pipe
1   │ total 28
2   │ drwxr-xr-x 4 leon leon 4096 Jan 10 15:57 hugo_cache
3   │ -rw------- 1 leon leon 9048 Jan  9 12:11 ip0L5
4   │ -rw-r--r-- 1 leon leon   69 Jan 10 15:20 remote-wsl-loc.txt
5   │ -rw-r--r-- 1 leon leon   14 Jan 31 11:43 some_file
6   │ prw-r--r-- 1 leon leon    0 Jan 31 11:37 test_pipe
7   │ -rw------- 1 leon leon 2662 Jan 10 15:21 vscode-distro-env.dIALVf
...

```

Both programs will exit. 



## Pipes vs temp files

Use a pipe if
- both programs read and write at roughly the same rate
- you only need to iterate over the data once
- you want the system to forget about the data at the earliest point possible

Use a temporary file if
- one program is much faster than the other (the faster one will need to wait due to the pipe blocking the main thread) 
- you need to iterate over the same data multiple times
- you want to keep the data after your programs are finished



## Python example

### Read and Write in the same process
```py
import os

if __name__ == "__main__":
    # Create a new pipe and get the two file descriptors
    read_fd, write_fd = os.pipe()

    # Write some bytes to the newly creates pipe
    bytes_written = os.write(write_fd, b"Hello, World!\n")
    # Close the file descriptor pointing to the pipe
    # If this line is missing, you need to rely on the reader to close the pipe correctly
    os.close(write_fd)

    # Start reading from the pipe (5 bytes each)
    while data := os.read(read_fd, 5):
        print(data)

```

### Read STDIN
```py
import sys

if __name__ == "__main__":
    # sys.stdin is a file descriptor pointing to a pipe
    # If the other end of the pipe is closed this blocks forever
    for line in sys.stdin:
        print(line)

```

### Named PIPE
```py
import errno
import os
import sys

if sys.platform == "win32":
    raise OSError("Named pipes only work on Linux")

PIPE_NAME = "/tmp/fancy_pipe"

try:
    # Create a new named pipe
    os.mkfifo(PIPE_NAME)
except OSError as e:
    if e.errno != errno.EEXIST:
        # Raise an error if the pipe could not be created and it does not already exist
        raise

# Open the file descriptor pointing to the pipe
# This blocks until the other end of the pipe is opened
print(f"Opening: {PIPE_NAME}")
with open(PIPE_NAME, "r") as pipe:
    # Start reading content from the pipe until it is empty
    print("Opened.")
    while data := pipe.read():
        if not len(data):
            print("Pipe is closed")
            break

        print(f"Read: {data}")

    os.unlink(PIPE_NAME)

```

This program blocks until you pass data to the pipe : ` echo "Hello, World" > /tmp/fancy_pipe`.