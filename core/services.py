from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import EmailLog, Registration


def send_registration_confirmation(registration: Registration) -> bool:
    if EmailLog.objects.filter(registration=registration, email_type='confirmation').exists():
        return False

    subject = 'You are in: From Zero to Momentum Webinar'
    message = render_to_string(
        'emails/registration_confirmation.txt',
        {
            'registration': registration,
            'event_name': 'From Zero to Momentum',
            'event_date': 'April 22, 2026',
            'event_time': '7:00 PM - 10:30 PM',
        },
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [registration.email])
    EmailLog.objects.create(registration=registration, email_type='confirmation', success=True)
    return True


def send_post_webinar_sequence(registration: Registration) -> int:
    sent = 0

    if not EmailLog.objects.filter(registration=registration, email_type='post_webinar_playbook').exists():
        message = render_to_string('emails/post_webinar_playbook.txt', {'registration': registration})
        send_mail(
            'Your Free Playbook is Ready',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [registration.email],
        )
        EmailLog.objects.create(
            registration=registration,
            email_type='post_webinar_playbook',
            success=True,
        )
        sent += 1

    if not EmailLog.objects.filter(registration=registration, email_type='post_webinar_offer').exists():
        message = render_to_string('emails/post_webinar_offer.txt', {'registration': registration})
        send_mail(
            'Next Steps: App, Community, Bootcamp, Consulting',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [registration.email],
        )
        EmailLog.objects.create(
            registration=registration,
            email_type='post_webinar_offer',
            success=True,
        )
        sent += 1

    return sent
