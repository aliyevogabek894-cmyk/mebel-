#!/bin/bash
set -e
echo '=== 1. Running Migrations ==='
python manage.py migrate --noinput
echo '=== 2. Initializing Admin & Data ==='
python init_db.py
echo '=== 3. Starting Gunicorn Web Server ==='
exec gunicorn mebel_erp.wsgi --bind 0.0.0.0:${PORT:-8080} --workers 2 --log-file -
