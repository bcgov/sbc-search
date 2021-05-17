## Install chart
cd ./devops/helm

helm dep up

helm install search-api . -f values-dev.yaml --namespace 6e0e49-dev

helm install search-api . -f values-test.yaml --namespace 6e0e49-test

helm install search-api . -f values-prod.yaml --namespace 6e0e49-prod
