#!/usr/bin/env bash

python manage.py crontab remove
killall -9 uwsgi
python manage.py makemigrations
python manage.py migrate
uwsgi --ini uwsgi.ini
python manage.py crontab add