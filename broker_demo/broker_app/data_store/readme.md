# imprcm data store container

This folder contains all the elements required to start the postgresql database container for the data store.

It uses a docker volume called `imprcm_data_store` to hold the database.


## First attempt
The database is initialised by the scripts in the `sql_scripts` folder if the volume is absent or empty. This creates the tables and populates the reference ones with starting data.

The container would normally be started using `docker compose` as part of the broker suite (see the `docker-compose.yml` file in the parent folder), but you can start it on its own using this powershell command:

```ps
docker run -p 5432:5432 -e POSTGRES_PASSWORD=fred -v D:/GithubRepos/IMPRCM/broker/docker_compose_demo/broker_app/data_store/sql_scripts:/docker-entrypoint-initdb.d -v imprcm_data_store:/var/lib/postgresql/data  --name imprcm_demo_datastore postgres
```

The data files in `sql_scripts` were created by dumping data from the demo database on `vivienne01` using commands like this:

```ps
psql -h vivienne01 -U pete -d imprcm_demo_ugms_touchdown -c 'COPY s_and_c_reference TO  stdout' | Out-file 's_and_c_reference.txt' -encoding ASCII
```



## Second attempt
The container is a specific image built using the `Dockerfile` in this folder. This copies the scripts into the startup folder on the container so it doesn't need to be mounted from outside and is thus portable.

Build it using a command like this:

```PS
docker build -t <your container name>:<your tag> .
```

Then run it using this variant of the run command:

```PS
docker run -p 5432:5432 -e POSTGRES_PASSWORD=fred -v imprcm_data_store:/var/lib/postgresql/data  --name imprcm_demo_datastore <your container name>:<your tag name>
```