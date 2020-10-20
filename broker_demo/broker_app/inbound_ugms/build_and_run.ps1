# build and run the container with specified input folder


docker build -t ugms_loader:latest .


# docker run  -it -v D:\GithubRepos\IMPRCM\broker\docker_compose_demo\broker_app\inbound_ugms\data:/data ugms_loader:latest #/bin/ash

docker rm --force ugms_loader

docker run --name ugms_loader -it -v D:\GithubRepos\IMPRCM\broker\docker_compose_demo\broker_app\inbound_ugms\data:/data ugms_loader:latest  /data/inbox  "host='vivienne01' port='15432' dbname='imprcm_demo_ugms_touchdown' user='imprcm_demo' password='imprcm_demo'"