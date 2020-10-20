# inbound ugms api using Camel and Maven

#FROM maven:latest

#RUN mkdir -p ugms_loader

#COPY ./camel/ugms-loader ugms_loader

#WORKDIR ugms_loader

#ENTRYPOINT ["mvn", "compile" "exec:java"]






# ugms file loader using python.  
FROM python:3-alpine

RUN mkdir -p /usr/src/ugms_loader
#RUN mkdir -p /data
WORKDIR /usr/src/ugms_loader

COPY ./ugms_file_loader /usr/src/ugms_loader

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip3 install --no-cache-dir -r requirements.txt && \
 apk --purge del .build-deps


ENTRYPOINT ["python3", "load_ugms_from_folder.py"]
