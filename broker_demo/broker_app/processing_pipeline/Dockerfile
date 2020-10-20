

FROM python:3-alpine

RUN mkdir -p /usr/src/data_processor
#RUN mkdir -p /data
WORKDIR /usr/src/data_processor

COPY ./python_processor /usr/src/data_processor

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip3 install --no-cache-dir -r requirements.txt && \
 apk --purge del .build-deps


ENTRYPOINT ["python3", "processing_pipeline.py"]
