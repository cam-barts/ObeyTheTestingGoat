#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir -p /code/logs
touch /code/logs/gunicorn.log
touch /code/logs/gunicorn-access.log
tail -n 0 -f /code/logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=superlists.settings

exec gunicorn superlists.wsgi:application \
     --name superlists \
     --bind 0.0.0.0:8000 \
     --workers 5 \
     --log-level=info \
     --log-file=/code/logs/gunicorn.log \
     --access-logfile=/code/logs/gunicorn-access.log \
"$@"