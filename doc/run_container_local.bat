:: windows batch file to run documentation docker container locally

:: prerequisites: Docker

:: parameters:
:: 
:: 1 - name of docker container
:: 2 - docker tag
:: 3 - local port to serve docs on

SETLOCAL 

SET container=%1
SET dockertag=%2
SET localport=%3
SET me=%~n0



@echo %me%: running container %container%, serving on http://localhost:%localport% as tag %dockertag%

:: stop and remove previous docker container and image
docker stop %dockertag%
docker rm %dockertag%

:: run new copy
docker run -d -p %localport%:80 --name %dockertag% %container%:%dockertag%

:: open it in the browser
start "" http://localhost:%localport%
