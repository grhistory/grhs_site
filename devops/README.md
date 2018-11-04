# Docker Dev Environment

The command `docker-compose up` will create three containers:

1. Web: Runs nginx to serve static assets and reverse-proxy the uwsgi app
1. App: Runs uwsgi to exectute django app
1. DB: Runs the postgres instance

You can also run `docker-compose up -d` to daemonize the process and free up your terminal for other usage. But that means you'll have to run `docker-compose -logs` to view any output from the containers (which can be useful for debugging).

Once the containers are running, application scripts (like migrations) can be ran using `docker-compose exec app <command>` within `./devops`. Convenience scripts are in the works to simplify this process.
