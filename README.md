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

These operations are done in the search_api container
```
flask db migrate

```

