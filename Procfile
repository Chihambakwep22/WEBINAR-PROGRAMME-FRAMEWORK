release: python manage.py migrate
web: gunicorn config.wsgi:application --bind 0.0.0.0:10000 --workers 2
