#!/usr/bin/env bash

set -o errexit

# TODO: Add args for triggering a rebuild, or only starting a specific app

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'docker-compose is safe to run even if the containers are already running. Note: The first run can take a while to download/build all the images and pull in dependencies.'

cd "./devops"

# TODO: Check if containers are already created. If so, run start instead of up
# This could be a little tricky, as multiple containers are managed by docker-compose
# so running `up` or `start` on everything might have issues depending on what other
# commands have been ran on individual containers beforehand. Until we have args
# available for rebuilding specific containers, we'll force a rebuild every time

docker-compose -p grhs_site up --build -d

echo 'Wait a moment and run the setup script manually (sorry).'
