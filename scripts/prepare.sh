#!/usr/bin/env bash

set -o errexit

BUILD_DEPS_IMAGE="grhistory/build_deps:1.0.0"
APP_DEPS_IMAGE="grhistory/app_deps:1.0.0"

echo 'Checking if the required Docker Images are available...'

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

# TODO: Better way to abstract this out/define name and path relationship?
if [[ "$(docker images -q $BUILD_DEPS_IMAGE 2> /dev/null)" == "" ]]; then
  echo "Build Dependencies Image does not exist, creating it..."
  docker build -t $BUILD_DEPS_IMAGE ./devops/dockerfiles/build-dependencies
else
  echo "Build Dependencies Image exists"
fi

if [[ "$(docker images -q $APP_DEPS_IMAGE 2> /dev/null)" == "" ]]; then
  echo "App Dependencies Image does not exist, creating it..."
  docker build -t $APP_DEPS_IMAGE -f ./devops/dockerfiles/app-dependencies/Dockerfile ./app/src
else
  echo "App Dependencies Image exists"
fi
