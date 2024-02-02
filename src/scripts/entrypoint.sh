#!/bin/bash

set -e

python manage.py collectstatic --noinput

wsgi --socket :8000 --master --enable-threads --module vertical_logistics.wsgi


