# build and run the demo IMPRCM broker using sensible defaults


## set the ports
$env:PORT_OBAPI=8089
$env:PORT_SDB=1543
$env:PORT_UUAPI=8086
$env:PORT_UDB=15433

docker-compose build


# bring the ensemble up and run in background
docker-compose up -d

# show the logs
docker-compose logs -t