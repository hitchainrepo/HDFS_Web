#!/usr/bin/env bash

python manage.py crontab remove
killall -9 uwsgi
uwsgi --ini uwsgi.ini
python manage.py crontab add