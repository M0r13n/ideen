# Operating System Structures

An operating system provides the environment in which programs are executed. It can be viewed from different vantage points:

- **focus on services that it provides**
- **focus on the interface that is provides**
- **focus in its components and interconnections**

## Operating System Services

- see page 60 in Silberschatzs Operating Systems
- user interface (e.g. GUI)
- program execution
- I/O (users typically can not control devices directly)
- file system

## Operating System Interface

- Command-line interface
  - allows the user to call programs
  - the interpreter used the name of the program to identify a file to be loaded into memory and executed
  - shell scripts are sets of commands recorded into a file
  - these shell scripts are not compiled into executable code, but are interpreted by the shell
- GUI
- Touch-Screen Interface

## System Calls

- interface to the services made available by the OS
- written in C, C++ and Assembly
- mostly hidden by an API (e.g. POSIX) from application programmers
  - available as a library of code (e.g. `libc`)
  - improve portability
- run-time environment is a suite of software needed to execute programs (compilers, interpreters and libraries)
  - provides a system call interface as the API
  - hides the implementation from the users of the API
- system calls are stored in a list index by their index
- three ways to pass parameters to the operating system:
  - less than five params: passed in registers
  - more than five params: stored in block in memory and the address of the block is passed as a register
  - params can be pushed onto a stack

### Examples

| Category          | Description                                                   | Examples                              |
|-------------------|---------------------------------------------------------------|---------------------------------------|
| Process Control   | create/terminate processes<br>wait/signal events              | `fork()`<br>`exit()`<br>`wait()`      |
| File Management   | create/delete files<br>read/write<br>attributes               | `open()`<br>`read()`<br>`write()`     |
| Device Management | request/release devices<br>read,write from devices            | `ioctl()`<br>`read()`<br>`write()`    |
| Maintainance      | get/set time<br>get process/file attributes                   | `getpid()`<br>`alarm()`<br>`sleep()`  |
| Communication     | create/delete communication channels<br>send/receive messages | `pipe()`<br>`shm_open()`<br>`mmap()`  |
| Portection        | get/set file permissions                                      | `chmod()`<br>`umask()`<br>`chown()`dd |
_(taken from page 71 of Silberschatz Operating Systems)_
