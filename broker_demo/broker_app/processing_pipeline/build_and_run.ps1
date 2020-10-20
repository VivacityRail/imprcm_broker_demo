# build and run the container with specified input folder


docker build -t data_processor:latest .


# docker run  -it -v D:\GithubRepos\IMPRCM\broker\docker_compose_demo\broker_app\inbound_ugms\data:/data ugms_loader:latest #/bin/ash

docker rm --force data_processor

docker run --name data_processor -it  data_processor:latest   "host='vivienne01' port='15432' dbname='imprcm_demo_ugms_touchdown' user='imprcm_demo' password='imprcm_demo'"