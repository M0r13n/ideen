# Docker Misc

## Docker network debugging

```bash
# Get an overview of all running containers and their networks
docker network ls
docker container ls
# Get the namespace id for a given container
docker inspect --format "{{ .State.Pid }}" <container_id>
# Enter the namespace
nsenter -n -t <ns_number>
```
