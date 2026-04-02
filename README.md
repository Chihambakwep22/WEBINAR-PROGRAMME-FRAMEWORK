# Webinar Programme Framework

A Django-powered webinar marketing and registration platform for "From Zero to Momentum".

## Features

- Landing page with hero, countdown, sponsors, and conversion CTA
- Speakers page with bios, key insights, and talk details
- Programme timeline page with session schedule
- Pricing tiers with highlighted recommendations
- Registration flow with:
  - duplicate email prevention
  - discount code validation
  - final price computation
- Registration success page with next-step links
- Post-webinar offers page with VIP-only filtering
- Playbook email lead capture form
- CTA click tracking endpoint for offer analytics
- Staff dashboard with filters and CSV export
- Django admin with Excel export for registrations
- Email automation:
  - registration confirmation
  - post-webinar follow-up sequence for attendees

## Tech Stack

- Python
- Django 6
- SQLite (default for development)
- openpyxl (Excel export)

## Project Structure

- config/: Django project settings and URL configuration
- core/: app models, forms, views, admin, services, commands
- templates/: HTML templates
- static/: CSS, JavaScript, and image assets

## Quick Start

1. Create and activate virtual environment
2. Install dependencies
3. Run migrations
4. Seed sample webinar data
5. Create admin user
6. Start server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_webinar_data
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Management Commands

Seed starter data:

```bash
python manage.py seed_webinar_data
```

Send post-webinar sequence:

```bash
python manage.py send_post_webinar_emails --dry-run
python manage.py send_post_webinar_emails
```

## Email Configuration

Default development backend prints emails to console.

To use SMTP, configure in config/settings.py:

- EMAIL_BACKEND
- EMAIL_HOST
- EMAIL_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- EMAIL_USE_TLS
- DEFAULT_FROM_EMAIL

## Deployment Notes

Before production:

- set DEBUG = False
- set ALLOWED_HOSTS
- use PostgreSQL instead of SQLite
- set secure SECRET_KEY from environment variable
- configure static/media file serving

## License

For learning and project use.
