#!/usr/bin/env bash

set -o errexit

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'Executing db migrations within the app container...'

cd "./devops"

docker-compose -p grhs_site exec app python manage.py migrate
