FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip3 install --no-cache-dir -r requirements.txt && \
 apk --purge del .build-deps


COPY . /usr/src/app

ENTRYPOINT ["python3", "-m", "imprcm_query_server"]
