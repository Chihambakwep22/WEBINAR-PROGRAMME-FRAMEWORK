from django.db import models


class Speaker(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    photo_url = models.URLField(blank=True)
    talk_title = models.CharField(max_length=200)
    key_insights = models.TextField(help_text='One insight per line.')
    extra_details = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self) -> str:
        return self.name


class TicketTier(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text='One feature per line.')
    is_highlighted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price']

    def __str__(self) -> str:
        return f'{self.name} (${self.price})'


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent_off = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    ticket_tier = models.ForeignKey(
        TicketTier,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Leave blank to allow all tiers.',
    )

    def __str__(self) -> str:
        return self.code


class Registration(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30)
    ticket_tier = models.ForeignKey(TicketTier, on_delete=models.PROTECT)
    discount_code = models.ForeignKey(
        DiscountCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    student_id_image = models.ImageField(upload_to='student_ids/', null=True, blank=True)
    final_price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_confirmed = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, blank=True)
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.full_name} <{self.email}>'

    def payment_message_draft(self) -> str:
        if not self.payment_confirmed:
            return 'Payment not yet confirmed.'

        return (
            f'Hi {self.full_name}, your payment for the From Zero to Momentum webinar has been confirmed. '
            f'Your seat is secured for April 22, 2026 from 7:00 PM to 10:30 PM. '
            f'Ticket: {self.ticket_tier.name}. Reference: {self.payment_reference or "N/A"}. '
            'Please keep this message for your record.'
        )


class ProgrammeSession(models.Model):
    SESSION_TYPES = [
        ('welcome', 'Welcome'),
        ('speaker', 'Speaker Session'),
        ('qa', 'Q&A'),
        ('closing', 'Closing'),
    ]

    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speaker = models.ForeignKey(Speaker, null=True, blank=True, on_delete=models.SET_NULL)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='speaker')
    color_hex = models.CharField(max_length=7, default='#1e5b4f')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['start_time', 'display_order']

    def __str__(self) -> str:
        return f'{self.title} ({self.start_time:%H:%M})'


class Sponsor(models.Model):
    name = models.CharField(max_length=120)
    logo_url = models.URLField()
    website = models.URLField(blank=True)
    description = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self) -> str:
        return self.name


class Offer(models.Model):
    OFFER_TYPES = [
        ('playbook', 'Playbook'),
        ('app', 'App'),
        ('community', 'Community'),
        ('event', 'Next Event'),
        ('consulting', 'Consulting'),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    cta_text = models.CharField(max_length=60, default='Learn More')
    cta_url = models.URLField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default='app')
    is_vip_only = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self) -> str:
        return self.title


class PlaybookLead(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.email


class ClickEvent(models.Model):
    event_type = models.CharField(max_length=50)
    session_key = models.CharField(max_length=40, blank=True)
    registration = models.ForeignKey(
        Registration,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class EmailLog(models.Model):
    EMAIL_TYPES = [
        ('confirmation', 'Confirmation'),
        ('post_webinar_playbook', 'Post Webinar Playbook'),
        ('post_webinar_offer', 'Post Webinar Offer'),
    ]

    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    email_type = models.CharField(max_length=40, choices=EMAIL_TYPES)
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-sent_at']
        unique_together = ('registration', 'email_type')
