#!/bin/sh
while ! nc -z app "$APP_DOCKER_PORT"; do sleep 3; done

nginx -g 'daemon off;'
