grhs_site
==================


Run postgresql:

* Mac: `brew services start postgresql`

```
make develop_env
# after server is running, ctrl-c 

source venv/bin/activate
make superuser

make runserver
```

Login:
* superuser
* pass


Docs: https://wagtail-cookiecutter-foundation.readthedocs.io/en/latest/


Redo initial_data.sql:

```
dropdb grhs_site
make db initial_data superuser
```
