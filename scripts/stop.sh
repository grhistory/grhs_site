#!/usr/bin/env bash

set -o errexit

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'Stopping Docker containers...'

cd "./devops"

docker-compose -p grhs_site stop
