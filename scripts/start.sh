#!/usr/bin/env bash

set -o errexit

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'docker-compose is safe to run even if the containers are already running. Note: The first run can take a while to download/build all the images and pull in dependencies.'

cd "./devops"

docker-compose up --build -d

echo 'Wait a moment and run the setup script manually (sorry).'
