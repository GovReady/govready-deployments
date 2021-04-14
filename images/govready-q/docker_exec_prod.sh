#!/usr/bin/env bash

/usr/local/bin/docker_exec_write_environment.sh

echo "[ + ] Running checks"
python3 manage.py check --deploy

echo "[ + ] Generating Static Files"
python3 manage.py collectstatic --noinput

echo "[ + ] Migrating Database"
python3 manage.py migrate
python3 manage.py load_modules
python3 manage.py first_run --non-interactive

# Start server
echo "[ + ] Starting server"
gunicorn --config /etc/opt/gunicorn.conf.py siteapp.wsgi