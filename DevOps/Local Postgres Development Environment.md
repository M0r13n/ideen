# How to setup a local development environment for Postgres

Installing Postgres sucks (so does every application). Therefore I run it inside a Container.

1. Create a local folder to persist the postgres data
`$ mkdir ${HOME}/postgres-data/`

2. Run a Postgres image

```
docker run -d \
	--name <NAME_IT> \
	-e POSTGRES_PASSWORD=<PASSWORD> \
	-v <PATH_TO_POSTGRES_FOLDER>/:/var/lib/postgresql/data \
        -p 5432:5432
        postgres
```

3. Verify it's running

`docker ps`

4. Connect

`docker exec -it  <NAME_IT> bash`