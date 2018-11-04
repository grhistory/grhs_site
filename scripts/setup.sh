#!/usr/bin/env bash

set -o errexit

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'Executing setup within app container...'

cd "./devops"

docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py copy_media
