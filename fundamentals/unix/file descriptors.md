# Unix File Descriptors

In simple terms a file descriptor is a key that points to an open file. The Kernel maintains a mapping of keys (as integers) and open files. If there are 20 open files your Kernel needs to keep a list of 20 entries. Then the File Descriptor 16 points to what ever file is associated with this key.

## Default Unix Files

| Name              | Number         |
| ------------- |:-------------:|
| STDIN            | 0                    |
| STDOUT        | 1                     |
| STDERR         | 2                    |

## Details
The key (integer) is managed by the Kernel. The Kernel calculates a number and returns this number when an `open` syscall is issued. In the most simplest implementation this key is an index into an array of open files  managed by the Kernel. A process **never** manages the file itself. Instead it keeps track of **only** file descriptors. All those low level details and abstractions are managed by Kernel, separated from userspace. 

**IMPORTANT** Each process keeps its **own unique** file descriptor table. So if we have two processes `A` and `B`, both processes have at least three file descriptors. This is because the default Unix File Descriptors are created automatically for every process. But the  file descriptors of process `A` are not the same as the ones from `B`. If they were the same files, it would be possible to write different input to different processes, because all processes would share the same `stdin`.

### Clone (duplicate) file descriptors
```py
import os

if __name__ == "__main__":
    # Create a copy of STDOUT
    new_fd = os.dup(1)

    # The newly created FD has a new number
    assert new_fd != 1

    # Close the original STDOUT
    os.close(1)

    try:
        print("Hello World")
    except OSError:
        # print writes to STDOUT by default
        # Because the file descriptor is closed an error as raised
        pass

    # But we can still write to the copy of STDOUT
    os.write(new_fd, b"Hello World")
```

See the above Python program. 

The program creates a copy of STDOUT. This syscall `dup` creates a new entry in your file structure in Kernel. Therefore it returns a **new** integer. Both keys (`1` and `3`) point to the same file, but are not the same. This means that closing STDOUT (file descriptor `1` does not change `new_fd`).

If we now close STDOUT, the file descriptor will be destroyed completely. There is not way back. 

## Pipes

[[pipes]] are pairs of file descriptors. The `pipe()` syscall returns two file descriptors. The first index is the read end of the pipe while the second index is the write end. 


