#!/usr/bin/env bash

set -o errexit

scriptdir="$(dirname "$0")"
cd "$scriptdir/.."

echo 'Executing setup within app container...'

cd "./devops"

docker-compose -p grhs_site exec app python manage.py migrate
docker-compose -p grhs_site exec app python manage.py copy_media
docker-compose -p grhs_site exec app python manage.py setup_basic_pages
docker-compose -p grhs_site exec app python manage.py create_baxter_award_pages
docker-compose -p grhs_site exec app python manage.py create_product_pages
docker-compose -p grhs_site exec app sh -c 'echo "from django.contrib.auth.models import User; User.objects.create_superuser(\"superuser\", \"superuser@example.com\", \"pass\")" | ./manage.py shell'
