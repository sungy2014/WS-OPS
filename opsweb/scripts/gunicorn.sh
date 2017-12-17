#!/bin/bash

NAME='wsops'
DJANGODIR='/ops-data/zp/haha/mysite-11/opsweb'
USER=root
GROUP=root
NUM_WORKERS=4

# reload the application server for each request
MAX_REQUESTS=100000

# which settings file should Django use
DJANGO_SETTINGS_MODULE=opsweb.settings

# WSGI module name
DJANGO_WSGI_MODULE=opsweb.wsgi

echo “Starting $NAME as `whoami`”

# Activate the virtual environment
cd $DJANGODIR
source /ops-data/zp/haha/mysite-11/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use –daemon)
exec /ops-data/zp/haha/mysite-11/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
-n ${NAME} \
-w 4 \
--max-requests ${MAX_REQUESTS} \
--user ${USER} \
--group ${GROUP} \
-b 127.0.0.1:10086 \
--log-level=error \
--log-file=/ops-data/zp/haha/mysite-11/opsweb/logs/gunicorn.log \
-D
