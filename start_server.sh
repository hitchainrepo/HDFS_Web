#!/usr/bin/env bash

killall -9 uwsgi
uwsgi --ini uwsgi.ini
python manage.py crontab add