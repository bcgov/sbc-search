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


## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Run your unit tests
```
yarn test:unit
```

### Lints and fixes files
```
yarn lint
```


