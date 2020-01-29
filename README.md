# sbc-search
BC Registries and Online Services search services

## Project setup (Docker)

Development
```
cp dc.dev.yml docker-compose.override.yml
docker-compose up
```
Browse to `localhost:8080`

Deployment
```
cp dc.prod.yml docker-compose.override.yml
docker-compose up
```
Browse to `localhost:8080`

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


