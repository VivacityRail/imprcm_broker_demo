# Outbound API

This folder is a dockerised version of the outbound API. It is based on the demo version from broker/api/sandc-query

Edit that app and copy changes to the `imprcm_query_server` folder.

build the app using `docker build -t imprcm_query_server:nrtest .` or a tag of your choice. The build will use the local Dockerfile.

run the database in a separate container (e.g. the database in the `broker_app\data_store` folder)

You can find out the IP address of the container by doing `docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" <db container name>`. Use this as the IP address for the connection string for the API.

If using `docker-compose`, the database server gets a virtual host name which you can use instead.

To connect to a running database set up on docker compose, you need to connect to its network using the `--network` flag of the `docker run` command.




