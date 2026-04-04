from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Offer, ProgrammeSession, Speaker, Sponsor, TicketTier


class Command(BaseCommand):
    help = 'Seed starter data for the webinar website.'

    def handle(self, *args, **options):
        TicketTier.objects.update_or_create(
            code='early-bird',
            defaults={
                'name': 'Early Bird',
                'price': 7,
                'description': 'Best value for early action takers.',
                'features': 'Live webinar access\nQ&A participation',
                'is_highlighted': True,
                'active': True,
            },
        )
        TicketTier.objects.update_or_create(
            code='standard',
            defaults={
                'name': 'Standard',
                'price': 10,
                'description': 'Complete webinar access.',
                'features': 'Live webinar access\nQ&A participation\nReplay access',
                'active': True,
            },
        )
        TicketTier.objects.update_or_create(
            code='vip',
            defaults={
                'name': 'VIP',
                'price': 22,
                'description': 'Premium acceleration package.',
                'features': 'Replay recording\nExecution template\nCommunity trial',
                'active': True,
            },
        )

        speaker1, _ = Speaker.objects.update_or_create(
            name='George Bassey',
            defaults={
                'role': 'Founder, Impactpreneur Global',
                'bio': 'Entrepreneurship educator helping founders scale with systems.',
                'photo_url': 'https://images.unsplash.com/photo-1562788869-4ed32648eb72?auto=format&fit=crop&w=600&q=80',
                'talk_title': 'Building Enterprise Discipline from Day One',
                'key_insights': 'Mindset to market translation\nExecution cadence\nPerformance loops',
                'extra_details': 'Practical frameworks for moving from idea to revenue.',
                'display_order': 1,
            },
        )
        speaker2, _ = Speaker.objects.update_or_create(
            name='Quantilytix Team',
            defaults={
                'role': 'Product and Growth Specialists',
                'bio': 'Helping professionals build growth systems with data-backed execution.',
                'photo_url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80',
                'talk_title': 'Personal Growth Systems that Compound',
                'key_insights': 'Personal operating system\nProductivity architecture\nFounder resilience',
                'extra_details': 'Real examples from African founders and creators.',
                'display_order': 2,
            },
        )

        dt = timezone.make_aware(datetime.fromisoformat('2026-04-22T19:00:00'))

        ProgrammeSession.objects.update_or_create(
            title='Welcome and Event Kickoff',
            defaults={
                'description': 'Context, expectations, and momentum framework.',
                'start_time': dt,
                'end_time': dt + timedelta(minutes=10),
                'session_type': 'welcome',
                'display_order': 1,
                'color_hex': '#d8a136',
            },
        )
        ProgrammeSession.objects.update_or_create(
            title=speaker1.talk_title,
            defaults={
                'description': 'Deep dive into enterprise execution discipline.',
                'start_time': dt + timedelta(minutes=10),
                'end_time': dt + timedelta(minutes=35),
                'session_type': 'speaker',
                'speaker': speaker1,
                'display_order': 2,
                'color_hex': '#0b3d2e',
            },
        )
        ProgrammeSession.objects.update_or_create(
            title=speaker2.talk_title,
            defaults={
                'description': 'Systems and habits for founder growth.',
                'start_time': dt + timedelta(minutes=35),
                'end_time': dt + timedelta(minutes=60),
                'session_type': 'speaker',
                'speaker': speaker2,
                'display_order': 3,
                'color_hex': '#c85a2e',
            },
        )
        ProgrammeSession.objects.update_or_create(
            title='Q&A and Closing',
            defaults={
                'description': 'Audience questions and next-step actions.',
                'start_time': dt + timedelta(minutes=60),
                'end_time': dt + timedelta(minutes=75),
                'session_type': 'qa',
                'display_order': 4,
                'color_hex': '#1f7a8c',
            },
        )

        Sponsor.objects.update_or_create(
            name='Impactpreneur Global',
            defaults={
                'logo_url': 'https://dummyimage.com/400x220/0b3d2e/ffffff&text=Impactpreneur+Global',
                'website': 'https://qx.quantilytix.co.za/',
                'description': 'Empowering African entrepreneurs to build sustainable ventures.',
                'active': True,
                'display_order': 1,
            },
        )
        Sponsor.objects.update_or_create(
            name='Quantilytix',
            defaults={
                'logo_url': 'https://dummyimage.com/400x220/c85a2e/ffffff&text=Quantilytix',
                'website': 'https://qx.quantilytix.co.za/',
                'description': 'Growth and productivity tools for founders and teams.',
                'active': True,
                'display_order': 2,
            },
        )

        Offer.objects.update_or_create(
            title='Free Momentum Playbook',
            defaults={
                'description': 'Download the practical execution workbook used during the webinar.',
                'cta_text': 'Download Playbook',
                'cta_url': 'https://example.com/playbook',
                'offer_type': 'playbook',
                'is_vip_only': False,
                'active': True,
                'display_order': 1,
            },
        )
        Offer.objects.update_or_create(
            title='Quantilytix App',
            defaults={
                'description': 'Move from planning to execution with guided daily focus systems.',
                'cta_text': 'Try the App',
                'cta_url': 'https://example.com/app',
                'offer_type': 'app',
                'is_vip_only': False,
                'active': True,
                'display_order': 2,
            },
        )
        Offer.objects.update_or_create(
            title='Premium 1:1 Consulting',
            defaults={
                'description': 'Private strategy sessions to map your next growth leap.',
                'cta_text': 'Book Consulting',
                'cta_url': 'https://example.com/consulting',
                'offer_type': 'consulting',
                'is_vip_only': True,
                'active': True,
                'display_order': 3,
            },
        )

        self.stdout.write(self.style.SUCCESS('Seed data completed.'))
