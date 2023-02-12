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


## Inspecting packages
Print the full package recipe:
`$  conan get <package>/<revision>@<user>/<channel>`

Print attributes of package:
` conan inspect <package>/<revision>@<user>/<channel>`

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


## Local Cache
By default Conan downloads all packages into your local cache under `~/.conan/data`. Packages can be removed from the local cache by:

```bash
$ conan remove "<package>" --force 
$ conan remove 'boost/\*'
$ conan remove 'MyPackage/1.2@user/channel'
```

## Using Packages as standalone applications
Packages run from your local cache by default. But they can also be run from your local project folder. This behavior can be customized through the `imports()` and `deploy()` functions.

```bash
$ conan install . -g=deploy # Copies all dependencies to local project folder
$ conan install . -g=virtualenv # Creates shell scripts to activate and deactivate environments
```


## Build Order
The “build-order” lists in order all the packages that needs to be built from sources. The logic is the following:
-   If a package is fully locked (it contains a package revision field `prev` in the lockfile), it will not be built from sources and will **never** appear in the build-order list.
-   If a package is not fully locked (it does **not** contain a package revision `prev` in the lockfile), it will appear in the build-order list. This situation happens both when the package binary doesn’t exist yet, or when the `--build` argument was used while creating the lockfile.

```bash
$ conan lock create ./conanfile.py            # Build only missing
$ conan lock create ./conanfile.py --build    # Build all dependencies
$ conan lock build-order ./conan.lock --build # Print build order
```

## Package Recipe
```py

class <Package>Conan(ConanFile):
    ...                                                # Various package metadata
    settings = "os", "compiler", "build_type", "arch"  # Defines available settings
    options = {"shared": [True, False]}                # Defines available options and defaults. "shared" is a common option which specifies whether a library is static or shared
    default_options = {"shared": False}
    requires = "RequiredLib/0.1@user/stable"           # Defines package requirements
    build_requires = "tool_a/0.2@user/testing"         # Defines requirements that are only used when the package is built. These should be build and test tools only.
    generators = "cmake"                               # Generator for the package: specifies which build system type will be generated

    def source(self):                                                # Obtains the source code for the project
        self.run("git clone https://github.com/conan-io/hello.git")  # self.run() executes any command in the native shell
        ...

    def build(self):                                                 # Responsible for invoking the build system
        cmake = CMake(self)                                          # Helper classes are available for several build systems
        ...
        if self.options.myoption1:                                   # Specify a conditional build requirement
            self.build_requires("zlib/1.2@user/testing")
        self.run("bin/unittests")                                    # Run unit tests compiled earlier in the build() method

    def package(self):                                               # Responsible for capturing build artifacts
        self.copy("\*.h", dst="include", src="hello")                # self.copy() copies files from the cache to the project folder
        ...

    def package_info(self):                                          # Responsible for defining variables that are passed to package consumers, for example library or include directories
        self.cpp_info.libs = ["hello"]                               # The cpp_info dictionary contains these variables
        ...

    def requirements(self):                                          # Responsible for specifying non-trivial requirements logic
        if self.options.myoption2:                                   # Specify a conditional requirement
            self.requires("RequiredLib2/0.3@user/stable")

    def package_id(self):                                            # Responsible for changing the way the package ID is calculated from the default
        default_package_id_mode = full_version_mode
        if self.settings.compiler.version == "4.9":                  # Make compiler versions 4.8 and 4.7 compatible with version4.9: i.e., they all result in the same package ID
            for version in ("4.8", "4.7"):
                compatible_pkg = self.info.clone()
                compatible_pkg.settings.compiler.version = version
                self.compatible_packages.append(compatible_pkg)      # The compatible_packages property is used to define this behaviour

    def imports(self):                                               # Copies dependency files from the local cache to the project directory
        ...

    def deploy(self):                                                # Installs the project, which can include copying build artifacts
        ...

```