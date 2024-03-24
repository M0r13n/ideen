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
| ----------------- | ------------------------------------------------------------- | ------------------------------------- |
| Process Control   | create/terminate processes<br>wait/signal events              | `fork()`<br>`exit()`<br>`wait()`      |
| File Management   | create/delete files<br>read/write<br>attributes               | `open()`<br>`read()`<br>`write()`     |
| Device Management | request/release devices<br>read,write from devices            | `ioctl()`<br>`read()`<br>`write()`    |
| Maintainance      | get/set time<br>get process/file attributes                   | `getpid()`<br>`alarm()`<br>`sleep()`  |
| Communication     | create/delete communication channels<br>send/receive messages | `pipe()`<br>`shm_open()`<br>`mmap()`  |
| Portection        | get/set file permissions                                      | `chmod()`<br>`umask()`<br>`chown()`dd |
_(taken from page 71 of Silberschatz Operating Systems)_

## Linkers and Loaders

1. Source Code (`main.c`) is compiled into an object file (`main.o`) using a command like `gcc -c main.c`. This step involves translating the human-readable code into machine-readable instructions, but not yet linking it with other object files or libraries.
2. The linker takes one or more object files (like `main.o`) and combines them together with any necessary libraries to create an executable file (e.g., `./main`). This step resolves symbols and addresses between different object files and libraries to create a complete program that can be run.
3. When the program (`./main`) is executed, the operating system's loader loads it into memory, along with any dynamically linked libraries it depends on. This process involves allocating memory for the program's code and data, resolving memory addresses, and setting up the program's execution environment.

## Application Binary Interface

The **ABI** defines how different components of binary code can interface for a given operating system on a given architecture.

## Monolithic Kernel

The Kernel provides the file system, CPU scheduling, memory management and other operating system functions through System Calls exposed through the System Call Interface to  user programs. The entire Kernel is compiled into a single address space, but the Linux Kernel does provide a modular design that allows runtime modifications.

## Microkernels


The operating system is condensed, and all nonessential components are removed from the kernel. Instead, these components are implemented in user space. This makes it easier to extend the OS because additional features can be implemented as user programs without modifications to the kernel. Also, such kernels tend to be more secure and reliable because services running as users do not compromise the rest of the system. On the downside, microkernels suffer from system-function overhead and message passing.
