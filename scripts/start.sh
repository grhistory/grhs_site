#!/usr/bin/env bash

set -o errexit

# TODO: Add args for triggering a rebuild, or only starting a specific app

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'docker-compose is safe to run even if the containers are already running. Note: The first run can take a while to download/build all the images and pull in dependencies.'

cd "./devops"

# TODO: Check if containers are already created. If so, run start instead of up

docker-compose up --build -d

echo 'Wait a moment and run the setup script manually (sorry).'
