# Conan for DevOps engineers

Conan is a packet manager for C++. It servers a similar purpose as pip in Python. 

## Conan Client
- Conan can be accesses via your terminal : `conan --version`
- it creates and consumes packages
- comes with a local cache (save bandwidth and enables offline use)

## Conan Remote
- can be either Bintray, Conan-Server or an Artifactory
- push and pull repositories

## Conan Package Identifier
A typical package identifier could look like this
```sh
$ libabc/1.0.4@elac/stable
```

It follows a pattern:

```sh
$ <PACKAGE_NAME>/<PACKAGE_VERSION>@<USER>/<CHANNEL>
```

#### PACKAGE_NAME
- Library Name
- can be any string

#### PACKAGE_VERSION
- Version identifier, e.g. `0.0.1`
- can be any string (also "ABCDEFG")

#### USER
- Package owner, e.g. `elac`
- the same package can be distributed by different users

#### CHANNEL
- identify **different packages** of the same library/project
- Example: `prod`, `stable`, `debug` or `etsting`

## Conan search

- Search inside your local cache (`~/.conan`):
```sh
$ conan search 
```

- Search on a remote, e.g. `conan-artifactory`:
```sh
$ conan search libabc -r conan-artifactory
```

- View details of a package:
```sh
$ conan search libabc/1.0.4@elac/stable -r conan-artifactory
```

- Generate a table view of the dependencies:
```sh
$ conan search libabc/1.0.4@elac/stable --table="some_table-html"
```

## Conan Info
This command gives you info about a given repo.

- List all dependencies
```sh
conan info .

# or

$ conan info libabc/1.0.4@elac/stable 

# or with a fancy graph

$ conan info libabc/1.0.4@elac/stable --graph=graph.html
```

## Conan install
- By hand from local cache
```sh
$ conan install libabc/1.0.4@elac/stable 
```

- By hand from remote
```sh
$ conan install libabc/1.0.4@elac/stable -r conan-artifactory
```

- By hand with custom generator, e.g. `cmake`
```sh
$ conan install libabc/1.0.4@elac/stable -g cmake -r conan-artifactory
```

- Normally you use a `conanfile.txt` (you can also use the `conanfile.py`, but I prefer to you a text file) to install a list of dependencies at once
```sh
# You may need to point to conan to the file expclictly if you are in a different folder
$ conan install .
```

- Commandline options overwrite the settings of the `conanfile`
```sh
# Overwrite what every stands in conanfile
$ conan install . -o *shared=True*

# Set Install folder
$ conan install . --install-folder ./install
```



## Conan profile
By default Conan will guess your settings. But you can override these settings by using profiles. 

- Create a new profile
```sh
# Create a new global profile under ~/.conan/profiles/
$ conan profile new fancy_profile --detect

# Create a profile in a folder
$ conan profile new ./fancy_profile --detect
```

The profile could look like:
```txt
[settings]
os=Linux
os_build=Linux
arch=x86_64
arch_build=x86_64
compiler=gcc
compiler.version=9
compiler.libcxx=libstdc++
build_type=Release

[options]
MyLib:shared=True

[build_requires]
libabc/1.0.4@elac/stable
libfancy/1.0.4@google/prod

[env]
# Here you can set custom variables that will be declared by conan
CC=/usr/bin/clang
CXX=/usr/bin/clang++
FANCY_VAR=42
```

- Inspect a profile
```sh
$ conan profile show fancy_profile
```

- Use a profile
```sh
$ conan install . -pr fancy_profile
```

- Use a profile and overwrite some values
```sh
$ conan install . -pr fancy_profile -s build_type=Debug
```


## Creating Packages
- Initialize a new conan package in an existing dir:
```sh
# Create a package called demo with version testing
$ conan new demo/testing
File saved: conanfile.py
```

- Create package
```sh
$ conan create .
Exporting package recipe
demo/testing: A new conanfile.py version was exported
...
```
`conan create` does a few things at once:
1.  Copy the sources to a new and clean build folder.
2.  Build the entire library from scratch.
3.  Package the library once it is built.
4.  Build the `test_package` example and test if it works.

`conan create` is equivalent to:
```sh
$ conan export . demo/testing
$ conan install libabc/0.1@demo/testing --build\=hello
```

`conan create` only creates a **LOCAL** copy. Which can be uploaded via:

```sh
conan upload libabc/1.2.3
```

## Packaging existing binaries
`conan create` will always run the `build()` method. Which is not always desired. The `export-pkg` method will just call `packe()` and `package_info`. 

- Example
```sh
$ conan export-pkg PATH/TO/conanfile.py hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...
```