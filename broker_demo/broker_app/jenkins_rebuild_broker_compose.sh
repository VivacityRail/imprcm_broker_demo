# script to rebuild the docker compose container group for the demo app

# set up the environment variables for the docker_compose.yml substitutions
# $PORT_SDB <- $JKN_COMPOSE_DATA_DB_PORT
# $PORT_OBAPI <- $JKN_COMPOSE_OUTBOUND_API_PORT
# $PORT_UDB <- $JKN_COMPOSE_UUID_DB_PORT
# $PORT_UUAPI <- $JKN_COMPOSE_UUID_SERVER_PORT

export PORT_SDB=$JKN_COMPOSE_DATA_DB_PORT
export PORT_OBAPI=$JKN_COMPOSE_OUTBOUND_API_PORT
export PORT_UDB=$JKN_COMPOSE_UUID_DB_PORT
export PORT_UUAPI=$JKN_COMPOSE_UUID_SERVER_PORT

echo data db port: $PORT_SDB
echo outbound api: $PORT_OBAPI
echo uuid db port: $PORT_UDB
echo uuid server:  $PORT_UUAPI
#echo `pwd`

cd ./broker/docker_compose_demo/broker_app
#echo `pwd`

# rebuild and restart the containers as they change
docker-compose build 
docker-compose up  -d --no-color