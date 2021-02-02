# govready-docker
Docker build of GovReady

## remove and rebuild image
docker rmi grq
docker build --tag grq .

## alternate build for debugging
docker build --tag grq --progress plain --no-cache .

## generic run command, drops into shell for further work
docker run -p8000:8000 -it --name grq grq bash

## generic run command, will run Dockerfile startup script (currently bash)
docker run -p8000:8000 -it --name grq grq
