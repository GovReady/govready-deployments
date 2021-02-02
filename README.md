# govready-docker
Docker build of GovReady

## remove and rebuild image
docker rmi grq ; docker build --tag grq .

## alternate build for debugging
docker build --tag grq --progress plain --no-cache .

## generic run command, drops into shell for further work
docker run -p8000:8000 -it --name grq grq bash

## generic run command, will run Dockerfile startup script (currently bash)
docker run -p8000:8000 -it --name grq grq

## run command with volume mounts
docker run -p8000:8000 -v `pwd`/log:/var/log -v `pwd`/config:/etc/opt -v `pwd`/local:/opt/govready-q/local -it --name grq grq

## run command with volume mounts, container removed after running
docker run --rm -p8000:8000 -v `pwd`/log:/var/log -v `pwd`/config:/etc/opt -v `pwd`/local:/opt/govready-q/local -it --name grq grq

## remove logs; run command with volume mounts, container removed after running
rm log/*log ; docker run --rm -p8000:8000 -v `pwd`/log:/var/log -v `pwd`/config:/etc/opt -v `pwd`/local:/opt/govready-q/local -it --name grq grq
