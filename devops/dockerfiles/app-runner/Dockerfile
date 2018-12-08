# docker-compose is going to set the context to the app directory (where the app source and config files will reside).
# So when we add files, it's based off 'app' being the context root, not the location of this Dockerfile

FROM node:10.13.0-alpine

LABEL maintainer="CJ Davis <cj@cjdavis.me>"
LABEL version="1.0.0"

COPY ./src/pages/static/ /opt/app

WORKDIR /opt/app

RUN npm i

FROM grhistory/app_deps:1.0.0

COPY ./src/ /opt/app/
COPY ./config/.env /opt/app/.env
COPY --from=0 /opt/app/node_modules /opt/app/pages/static/node_modules

RUN addgroup uwsgi && adduser -D -G uwsgi uwsgi
RUN chown -R uwsgi:uwsgi .

USER uwsgi

CMD [ "uwsgi", "--socket", "0.0.0.0:8080", \
    "--uid", "uwsgi", \
    "--protocol", "uwsgi", \
    "--wsgi", "grhs_site.wsgi:application" ]
