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
SET init=%3
SET localport=%4
SET datavolume=%5
SET me=%~n0



@echo %me%: running container %container% with data volume %datavolume%, serving on http://localhost:%localport% as tag %dockertag% and init=%init%

:: stop and remove previous docker container and image
docker stop %dockertag%
docker rm %dockertag%

:: if init is 1, re-initialise. This means delete the data volume
if %init%==1 docker volume rm %datavolume%


:: run new copy
docker run -d -p %localport%:5432 -e POSTGRES_PASSWORD=fred -v %datavolume%:/var/lib/postgresql/data --name %dockertag%      %container%:%dockertag%
