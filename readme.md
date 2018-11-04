# grhs_site

Run postgresql:

- Mac: `brew services start postgresql`

```
make develop_env
# after server is running, ctrl-c

source venv/bin/activate
make superuser

make runserver
```

Login:

- superuser
- pass

Docs: https://wagtail-cookiecutter-foundation.readthedocs.io/en/latest/

Redo initial_data.sql:

```
dropdb grhs_site && make db initial_data migrate extra_data superuser
```

## Docker Environment

We're using Docker to run the application on the production server (and it can be used for development as well). Docker installations instructions can be found [here](https://docs.docker.com/install/), with Ubuntu-specific instructions (for the production VM) [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/). Docker compose install instructions can be found [https://docs.docker.com/compose/install/#install-compose](here).

A `.env` is used to define configuration variables for the application and for the Docker build. It should reside in the `./app/config` directory. A `.env-template` file is provided to list the currently-used variable names.

To help speeed up the rebuild process on app changes, the app image has been split up into multiple images. Details can be seen within the `./devops/` directory. TODO: Add some scripts for creating supporting image.

### Starting the App

Once the `.env` file is set up, and all the supporting images have been created, docker-compose can handle all the rest. Some scripts are available as wrappers around the complexity of app executions.

- `prepare.sh` Will check to see if the necessary application images are available (that aren't pulled down from Docker hub), and build them if they aren't.
- `start.sh` Will build/pull the required images and start all the containers. TODO: Add args for specifying if images should rebuilt, and if only a certain app should be started.
- `stop.sh` Will stop all running containers. TODO: Add args for specifying only a specific app should be stopped.
- `setup.sh` Will execute commands that can't run until all the containers are fully up and running (i.e. running database migrations)
- `destroy.sh` Will tear down all the running containers. Volumes and images will still remain, so restarting the containers won't take as long.
