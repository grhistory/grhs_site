# docker-compose is going to set the context to the app directory (where the app source and config files will reside).
# So when we add files, it's based off 'app' being the context root, not the location of this Dockerfile

FROM node:10.13.0-alpine

COPY ./src/pages/static/ /opt/app

WORKDIR /opt/app

RUN npm i

FROM python:3.7.1-alpine

COPY ./src /opt/app
COPY ./config/.env /opt/app/.env
COPY --from=0 /opt/app/node_modules /opt/app/pages/static/node_modules

WORKDIR /opt/app

RUN addgroup uwsgi && adduser -D -G uwsgi uwsgi
RUN chown -R uwsgi:uwsgi .

# See https://stackoverflow.com/a/47871121/1324851 for why we need the extra packages
# jpeg-dev and zlib-dev are needed for Pillow
# g++ is needed for gcc to compile libsass
# linux-headers is needed for uWSGI to use linux/limits.h
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc postgresql-dev jpeg-dev zlib-dev g++ linux-headers && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

CMD [ "uwsgi", "--socket", "0.0.0.0:8080", \
    "--uid", "uwsgi", \
    "--protocol", "uwsgi", \
    "--wsgi", "grhs_site.wsgi:application" ]
