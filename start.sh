#!/bin/bash
set -e

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -w 5 -t 60 -b 0.0.0.0:8000 pmsearchapi.wsgi
