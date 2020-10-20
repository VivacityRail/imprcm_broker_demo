:: windows batch file to build documentation using sphinx, then build to docker image and run locally
:: makes the build include "todo" items.

:: prerequisites: Sphinx, Docker

:: parameters:
:: 
:: 1 - source folder
:: 2 - name of docker container
:: 3 - docker tag
:: 4 - local port to serve docs on

SETLOCAL 

SET sourcefolder=%1
SET container=%2
SET dockertag=%3
SET localport=%4
SET me=%~n0



echo %me%: building docs from %sourcefolder% to container %container%, serving on http://localhost:%localport% as tag %dockertag%

:: Run Sphinx to build the files from the .rst files in docs to html in docs/_build
sphinx-build -a -b html -D todo_include_todos=1 %sourcefolder% %sourcefolder%/_build

:: stop and remove previous docker container and image
docker stop %dockertag%
docker rm %dockertag%
powershell -command "& docker images -q %container%:* | ForEach {docker rmi -f "$_" }"

:: Build the docker container, running the makefile that copies the source html, js and -static in, binding to nginx 
docker build -t %container%:%dockertag% .

:: push to VivacityRail Docker repository (assumes we're logged in)
:: docker tag webserver:%container% vivacityrail/imprcm-docs:%dockertag%
:: docker push vivacityrail/imprcm-docs:%dockertag%


:: run new copy
docker run -d -p %localport%:80 --name %dockertag% %container%:%dockertag%

:: open it in the browser
start "" http://localhost:%localport%
