#!/bin/bash
 
NAME="EatHub"                                     # Name of the application
DJANGODIR=/eathub/eathub-webapp/                  # Django project directory
SOCKFILE=/eathub/eathub-webapp/run/gunicorn.sock  # we will communicte using this unix socket
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=eathub.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=eathub.wsgi                     # WSGI module name
 
echo "Starting $NAME as `whoami`"
 
# Activate the virtual environment
cd $DJANGODIR
source /eathub/eathub-webapp/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
 
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=debug \
  --bind=unix:$SOCKFILE
