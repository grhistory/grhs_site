FROM python:3.7.1-alpine

LABEL maintainer="CJ Davis <cj@cjdavis.me>"

# See https://stackoverflow.com/a/47871121/1324851 for why we need the extra packages
# jpeg-dev and zlib-dev are needed for Pillow
# g++ is needed for gcc to compile libsass
# linux-headers is needed for uWSGI to use linux/limits.h
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc postgresql-dev jpeg-dev zlib-dev g++ linux-headers
