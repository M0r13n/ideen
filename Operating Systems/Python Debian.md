# Python Debian

[Debian](./Creating%20Debian%20Packages.md) packages are useful for Python projects. A relatively straight forward approach for creating them:

- see [pyais-debian](https://github.com/M0r13n/pyais-debian) as a practical example
- use [pybuild](https://wiki.debian.org/Python/Pybuild) as the build system
- use Docker to build the package
- use [bind-mounts](../DevOps/Docker-Volumes.md#bind-mounts) to share files between host and container
  - use three mounts to make life easier:
    1. `./sources `--> `/source-ro/`
    2. `./output` --> `/output/`
    3. `./buildhelper.sh` --> `/buildhelper.sh`

Inside the container the contents of /source-ro/ are copied into /build/source, in which dpkg-buildpackage builds the package. This will write the built packages into the parent folder /build/, from which they are copied to /output. The latter is bind-mounted to share the files between container and host.

## Important files

### Dockerfile

Use a simple docker file with the required dependencies:

```Dockerfile
ARG distro="ubuntu:latest"

FROM ${distro}

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-all \
    python3-setuptools \
    python3-pip \
    python3-attr \
    python3-bitarray \
    dh-python \
    debhelper \
    build-essential
```

### debian/control

Use **python3-all** for packages targeting Python3. Also list dependencies in `Depends: python3-attr, python3-bitarray`.

```txt
Source: pyais
Section: python
Priority: extra
Maintainer: Leon Morten Richter <github@leonmortenrichter.de>
Build-Depends: debhelper-compat (= 13),
               dh-python,
               python3-all,
               python3-setuptools,
               python3-attr,
               python3-bitarray
Standards-Version: 3.9.5
Homepage: https://github.com/M0r13n/pyais

Package: pyais
Architecture: any
Pre-Depends: dpkg (>= 1.16.1), python3 ${misc:Pre-Depends}
Depends: ${misc:Depends}, ${python3:Depends}, ${shlibs:Depends}, python3-attr, python3-bitarray
Description: AIS message encoding and decoding in Python.
```

### debian/rules

```Makefile
#!/usr/bin/make -f

export PYBUILD_NAME=pyais
export DEB_BUILD_OPTIONS=nocheck

%:
	dh $@ --with python3 --buildsystem=pybuild
```

### build-helper.sh

```bash
/bin/bash -e

# This script is executed within the container as root.  It assumes
# that source code with debian packaging files can be found at
# /source-ro and that resulting packages are written to /output after
# succesful build.  These directories are mounted as docker volumes to
# allow files to be exchanged between the host and the container.

# Make read-write copy of source code
mkdir -p /build
cp -a /source-ro /build/source
cd /build/source

# Build the package
dpkg-buildpackage -us -uc -b

# `dpkg-buildpackage` places the built artifacts in the parent directory
# (../). Thus, copy all relevant built artifacts from /build/ to /output/.
cp -a /build/*.deb /build/*.buildinfo /build/*.changes /output/
ls -l /output
```

## Where is installed meta-data stored?

On Ubuntu 22.04 the package meta-data can be found here:

`/var/lib/dpkg/info/`

I already had to edit the `.postinst` file from this dir in order to remove a package.
