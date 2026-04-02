# From Zero to Momentum Webinar Website

Django-powered website with HTML frontend and full backend workflows for event conversion.

## Implemented Features

- Home landing page with hero hook, event identity, CTA, countdown, and sponsors section
- Speakers page with bios, topics, key insights, and expandable details
- Programme page with timeline schedule
- Pricing page with highlighted tier cards
- Registration form with:
  - duplicate email prevention
  - ticket tier selection
  - discount code support
  - final price computation
- Post-webinar offers page with optional VIP-only offers
- Playbook lead capture form
- Click tracking endpoint for CTA analytics
- Admin backend:
  - registration table
  - list filters (ticket tier, date, payment, attendance)
  - search by name/email/phone
  - Excel export action
- Staff dashboard view with filtering and CSV export
- Email automation:
  - immediate registration confirmation
  - post-webinar sequence command for attended users

## Project Structure

- `config/`: Django project config
- `core/`: main app models, views, forms, admin, services
- `templates/`: HTML templates
- `static/`: CSS and JS

## Run Locally

1. Activate environment (already created):
   - `.venv/bin/activate`
2. Install deps:
   - `pip install -r requirements.txt`
3. Apply migrations:
   - `./.venv/bin/python manage.py migrate`
4. Seed starter content:
   - `./.venv/bin/python manage.py seed_webinar_data`
5. Create admin user:
   - `./.venv/bin/python manage.py createsuperuser`
6. Start server:
   - `./.venv/bin/python manage.py runserver`

## Email Settings

Current setup uses Django console email backend for development.
To use SMTP, update in `config/settings.py`:

- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`

## Post-Webinar Email Sequence

Send to attendees marked as `attended=True`:

- Dry run: `./.venv/bin/python manage.py send_post_webinar_emails --dry-run`
- Actual send: `./.venv/bin/python manage.py send_post_webinar_emails`

## Integrations You Can Add Next

- Stripe/PayPal payment checkout and webhook-based payment confirmation
- Zoom auto-join links per registration
- Google Analytics / Meta Pixel scripts in base template
- SMS reminders for registered attendees
