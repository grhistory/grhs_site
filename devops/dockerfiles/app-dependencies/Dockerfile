FROM grhistory/build_deps:1.0.0

LABEL maintainer="CJ Davis <cj@cjdavis.me>"
LABEL version="1.0.0"

RUN mkdir -p /opt/app

COPY ./requirements.txt /opt/app/
COPY ./requirements /opt/app/requirements

RUN python3 -m pip install -r /opt/app/requirements.txt --no-cache-dir

WORKDIR /opt/app
