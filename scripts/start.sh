#!/usr/bin/env sh
set -e

echo "Waiting for database and running migrations..."
ATTEMPTS=20
COUNT=1
while [ "$COUNT" -le "$ATTEMPTS" ]; do
  if python manage.py migrate --noinput; then
    echo "Migrations applied successfully."
    break
  fi
  echo "Migration attempt $COUNT/$ATTEMPTS failed. Retrying in 5s..."
  COUNT=$((COUNT + 1))
  sleep 5
done

if [ "$COUNT" -gt "$ATTEMPTS" ]; then
  echo "Database did not become ready in time."
  exit 1
fi

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000 --workers "${WEB_CONCURRENCY:-1}"
