#!/bin/bash
# build docker container 

# uses $JKN_DOCKER_CONTAINER and $JKN_DOCKER_DOCKERTAG

echo running container $JKN_DOCKER_CONTAINER with tag $JKN_DOCKER_DOCKERTAG on local port $JKN_DOCKER_LOCALPORT

# stop and remove the container if it exists
docker ps -aq --filter="name=$JKN_DOCKER_DOCKERTAG" | grep -q . && docker stop $JKN_DOCKER_DOCKERTAG && docker rm $JKN_DOCKER_DOCKERTAG

docker run -d -p $JKN_DOCKER_LOCALPORT:80 --name $JKN_DOCKER_DOCKERTAG $JKN_DOCKER_CONTAINER:$JKN_DOCKER_DOCKERTAG
