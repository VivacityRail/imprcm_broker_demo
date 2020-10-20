@echo off
:: windows batch file to build docker image

:: prerequisites: Docker

:: parameters:
:: 
:: 1 - name of docker container
:: 2 - docker tag

SETLOCAL 

SET container=%1
SET dockertag=%2
SET me=%~n0



@echo %me%: building container %container% with tag %dockertag%
@echo .

:: stop and remove previous docker container and image
docker stop %dockertag%
docker rm %dockertag%
powershell -command "& docker images -q %container%:* | ForEach {docker rmi -f "$_" }"

:: Build the docker container based on Dockerfile
docker build -t %container%:%dockertag% .
