#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir logs
touch ./logs/gunicorn.log
touch ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=zed.settings

exec /usr/local/bin/gunicorn zed.wsgi:application \
    --name zed \
    --bind unix:zed.sock \
    --workers 3 \
    --log-level=info \
    --log-file=./logs/gunicorn.log \
    --access-logfile=./logs/access.log &

exec service nginx start



