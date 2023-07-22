# Docker Verify  Image

Container image integrity has become increasingly important as images are being deployed into zero-trust environments.

1. `docker pull python:3.11`
2. `docker buildx imagetools inspect python:3.11`
	1. `docker images --digests` does [not work](https://github.com/docker/hub-feedback/issues/1925)
	2. "*The digest displayed by the CLI is the digest of manifest list that composes of multiple manifests each representing an image for a particular platform. The digests shown in Hub are digests of each of these platform images.*"
3. verify the digest on the hub