# Docker ARG

*ARG* are also known as **build-time variables**. They are only available from the moment they are ‘announced’ in the Dockerfile with an **ARG** instruction up to the moment when the image is built. Running containers can’t access values of ARG variables. This also applies to CMD and ENTRYPOINT instructions which just tell what the container should run by default. If you tell a Dockerfile to expect various **ARG** variables (without a default value) but none are provided when running the build command, there will be an error message.

```Dockerfile
# default ARG that can be overridden
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

Can be build with:

`docker build -t pyais-debian . -f Dockerfile --build-arg distro=ubuntu:jammy`
