FROM grhistory/build_deps:latest

RUN mkdir -p /opt/app

COPY ./requirements.txt /opt/app/
COPY ./requirements /opt/app/requirements

RUN python3 -m pip install -r /opt/app/requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

WORKDIR /opt/app
