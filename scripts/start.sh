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

echo "Seeding webinar content..."
python manage.py seed_webinar_data

echo "Ensuring admin account from environment variables..."
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

username = os.getenv('DJANGO_SUPERUSER_USERNAME', '').strip()
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '').strip()
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com').strip() or 'admin@example.com'

if username and password:
    User = get_user_model()
    user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save()
    print(f'Admin user ensured: {username}')
else:
    print('DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set; skipping admin ensure.')
PY

echo "Starting gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:"${PORT:-10000}" --workers "${WEB_CONCURRENCY:-1}"
