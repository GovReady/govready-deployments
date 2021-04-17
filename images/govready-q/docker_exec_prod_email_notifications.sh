#!/usr/bin/env bash

/usr/local/bin/docker_exec_write_environment.sh

# Start server
echo "[ + ] Starting server"
python3 manage.py send_notification_emails forever