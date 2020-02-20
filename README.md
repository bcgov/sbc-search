# sbc-search
BC Registries and Online Services search services

## Project setup (Docker)

Development
```
cp dc.dev.yml docker-compose.override.yml
cp frontend/example.env frontend/.env
docker-compose up
```
Browse to `localhost:8080`

Deployment
```
cp dc.prod.yml docker-compose.override.yml
docker-compose up
```
Browse to `localhost:8080`

Updating database and create mock data
```
dx search_api (in nother terminal, to access the container)
flask db upgrade (to run existing migrations and update de db)
python bootstrap.py to create mock data
```

## connecting openshift

Download openshift from https://www.okd.io/download.html

unzip the oc binary, and run

```
oc port-forward bc-reg-fdw-indy-cat-6-ct8z5 5432:5432
```

```
apt-get install nmap
ncat -l 0.0.0.0 15432 --keep-open --sh-exec "ncat localhost 5432"
```

## Migrations

This project uses
  * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
  * [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/), based on alembic.

These operations are done in the search_api container

To initially get your DB up to date:
```
flask db upgrade
```

To create new migration scripts
```
flask db migrate
git add
```


