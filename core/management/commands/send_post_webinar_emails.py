from django.core.management.base import BaseCommand

from core.models import Registration
from core.services import send_post_webinar_sequence


class Command(BaseCommand):
    help = 'Send post-webinar email sequence to attendees marked as attended.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only show how many emails would be sent.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        attendees = Registration.objects.filter(attended=True)

        total = 0
        for reg in attendees:
            if dry_run:
                self.stdout.write(f'Would send to: {reg.email}')
                continue
            total += send_post_webinar_sequence(reg)

        if dry_run:
            self.stdout.write(self.style.WARNING(f'Dry run complete. {attendees.count()} attendees matched.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Completed. {total} post-webinar emails sent.'))
