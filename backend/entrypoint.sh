#!/bin/bash
set -e

echo "[ENTRYPOINT] Waiting for DB..."

until python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conduit.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
"; do
  echo "DB not ready yet..."
  sleep 2
done

echo "[ENTRYPOINT] Apply migrations..."
python manage.py migrate --noinput

echo "[ENTRYPOINT] Starting server..."
exec "$@"