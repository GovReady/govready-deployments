#!/usr/bin/env bash

/usr/local/bin/docker_exec_write_environment.sh
python3 /etc/opt/wait-for-database.py

echo "[ + ] Running checks"
python3 manage.py check --deploy

echo "[ + ] Generating Static Files"
python3 manage.py collectstatic --noinput

echo "[ + ] Migrating Database"
python3 manage.py migrate
python3 manage.py load_modules
python3 manage.py first_run --non-interactive

# Aspen upgrades if installing aspen version
FILE=siteapp/management/commands/upgrade_aspen.py
if test -f "$FILE"; then
    echo "[ + ] Applying Aspen configuration upgrades"
    python3 manage.py upgrade_aspen --non-interactive
fi

# Start server
echo "[ + ] Starting server"
gunicorn --config /etc/opt/gunicorn.conf.py siteapp.wsgi