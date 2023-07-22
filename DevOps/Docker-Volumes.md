# Docker-Volumes

There are two fundamental ways of persisting data in Docker: **bind mounts** and **volumes**. By default all files created inside a container are stored on a writable container layer. This implies that:

- data is not persisted when a container is stopped
- data can not easily be moved

## Bind mounts

- mount **any** host path inside the container
- basically shares a folder between a host and a container
- **both**, the host **and** the container can read/write to this folder
- I typically use it to copy a configuration file into a container
- also great to share source code or build artifacts
- Syntax: `./path/to/host/folder:/path/inside/container`
- docker-compose.yml could look like:

```yaml
  mktxp:
    image: leonmorten/mktxp:latest
    volumes:
      - './mktxp/:/home/mktxp/mktxp/'
```

A potential downside is that the folder is shared between the host and the container. Thus, there is no clear isolation between the two. This means that if the file(s) on the host are changed, deleted or corrupted the data inside the container is also affected (this also affects file permissions!). **This is a powerful ability which can have security implications, including impacting non-Docker processes on the host system.**

## Volumes

- managed by Docker itself
- works like a virtual hard drive that can be mounted inside the container
- volumes are **not accessible** from the host computer
- volumes are stored on the host under `/var/lib/docker/volumes/`
- can be used to back up, restore, or migrate data from one Docker host to another
- faster (I/O, latency, throughput) that binds
- docker-compose.yml could look like:

``` yaml
version: "3.9"

volumes:
	# The volume needs to be explicitely mentioned in the volumes array
    prometheus_data: {}

  grafana:
    image: grafana/grafana
    container_name: grafana
    volumes:
      # The volume is then mounted under a given path inside the container
      - grafana_data:/var/lib/grafana
```

