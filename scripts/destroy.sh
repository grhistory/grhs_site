#!/usr/bin/env bash

set -o errexit

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'Stopping and removing Docker setup...'

cd "./devops"

docker-compose down
