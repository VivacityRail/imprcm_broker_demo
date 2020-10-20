#!/bin/bash
# build docker container 

# uses $JKN_DOCKER_CONTAINER and $JKN_DOCKER_DOCKERTAG


# @echo %me%: building container %container% with tag %dockertag%
# @echo .

# :: stop and remove previous docker container and image
# docker stop %dockertag%
# docker rm %dockertag%
# powershell -command "& docker images -q %container%:* | ForEach {docker rmi -f "$_" }"

# :: Build the docker container based on Dockerfile
# docker build -t %container%:%dockertag% .

echo building container $JKN_DOCKER_CONTAINER with tag $JKN_DOCKER_DOCKERTAG using docker file $JKN_DOCKER_DOCKERFILE

# note you need to make sure jenkins has access to docker before docker commands will work.
# This needs `sudo usermod -a -G docker jenkins` followed by jenkins restart 

docker build -q -t $JKN_DOCKER_CONTAINER:$JKN_DOCKER_DOCKERTAG -f docsource/$JKN_DOCKER_DOCKERFILE docsource/
