# Docker Images

Docker uses storage drivers to store **image layers**, and to store data in the **writable layer of a container**. The container’s writable layer does **not persist after the container is deleted**, but is suitable for storing ephemeral data that is generated at runtime.

![container layer are based on commands in the Dockerfile](assets/layers.png)

- images are built up from a series of layers
- each layer represents an instruction in die Dockerfile
- commands, that modify the filesystem, create a new layer
- each layer is the set of differences from the layer before it (similar to Commits)
- existing layers are reused whenever possible
- if a command changes its layer changes and all layers after this layer also have to update
  - this is not always wanted
  - consider a `COPY . .` at the beginning of the Dockerfile
  - every time this command is executed all layers coming after it have to rebuild
  - prevented, by careful ordering of instructions in the Dockerfile
- chain multiple operations in a single `RUN` command to reduce **layer bloat**
- helpful: `docker inspect grafana/grafana:latest | jq -r '.[].RootFS'`
- do not confuse **base images** with **parent images**
  - a [parent image](https://docs.docker.com/glossary/#parent-image) is the image that your image is based on
  - a  [base image](https://docs.docker.com/glossary/#base-image) has `FROM scratch` in its Dockerfile.

## Containers and Layers

![container writable layer](assets/sharing-layers.jpg)

- major difference between a container and an image is the top writable layer
- any changes that modify the filesystem during the containers lifetime are stored in a thin writable layer
- the lifetime of the writable layer is bound to the lifetime of the container
  - when the container is deleted, the writable layer is also deleted
- the image is never changed
  - multiple containers can re-use the same image without manipulating it
- use [volumes](./Docker-Volumes.md) to persist data or share data between containers

## Multi-stage builds

- remember: each command in the Dockerfile results in a new layer

- reduce the total number of layers by

  - ordering commands  from the less frequently changed to the more frequently changed

  - by calling `FROM scratch` at the end:

    ```dockerfile
    # This results in a single layer image
    FROM scratch
    COPY --from=build /bin/project /bin/project
    ENTRYPOINT ["/bin/project"]
    CMD ["--help"]
    ```

## Example

```bash
$ docker pull alpine:3.17
# ...
Pulling from library/alpine
Digest: sha256:e95676db9e4a4f16f6cc01a8915368f82b018cc07aba951c1bd1db586c081388
#...
$ docker pull grafana/grafana:latest
latest: Pulling from grafana/grafana
4db1b89c0bd1: Already exists 
312681f4cad0: Pull complete 
8b7b65888846: Pull complete 
# ...
5c0c2b741753: Pull complete 
Digest: sha256:423040d62678074111e4e72d7dcef23480a94eb4f21b9173204d1a5ee972ec59
$ docker image inspect grafana/grafana:latest
"sha256:3dab9f8bf2d28c8bd1047f3ac2d0c72f3570562f491e67ef8179dfdcc68bccff",
"sha256:a264d9aaf8ec716fc33817ac815be263239adac15fa104f7b2bb2b7ae2dcb043",
"sha256:8bc5f72040860da1f4847b339b3b58cf7cefb12a0b3ce9e2e41d5d72e4b303da",
"sha256:f7034fba314317a6883def50d59ba6e7e29dd0c5717bc386116f4ba120d10e23",
$ docker image inspect alpine:3.17
"sha256:3dab9f8bf2d28c8bd1047f3ac2d0c72f3570562f491e67ef8179dfdcc68bccff"

```

- grafana/grafana is based in alpine
- pulling alpine first and then pulling grafana afterwards shows that the alpine layer is resused