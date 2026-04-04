from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from openpyxl import Workbook

from .models import (
    ClickEvent,
    DiscountCode,
    EmailLog,
    Offer,
    PaymentMethod,
    PlaybookLead,
    ProgrammeSession,
    Registration,
    Speaker,
    Sponsor,
    TicketTier,
)


@admin.action(description='Export selected registrations to Excel')
def export_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Registrations'
    ws.append(['Name', 'Email', 'Phone', 'Tier', 'Payment Method', 'Final Price', 'Paid', 'Attended', 'Created'])

    for row in queryset.select_related('ticket_tier', 'payment_method'):
        ws.append(
            [
                row.full_name,
                row.email,
                row.phone_number,
                row.ticket_tier.name,
                row.payment_method.name if row.payment_method else '',
                float(row.final_price),
                row.payment_confirmed,
                row.attended,
                row.created_at.isoformat(),
            ]
        )

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=registrations.xlsx'
    wb.save(response)
    return response


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'ticket_tier',
        'payment_method',
        'final_price',
        'payment_confirmed',
        'student_id_uploaded',
        'attended',
        'created_at',
    )
    list_filter = ('ticket_tier', 'payment_method', 'payment_confirmed', 'attended', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    readonly_fields = ('student_id_preview', 'payment_message_preview')
    actions = [export_to_excel]

    @admin.display(boolean=True, description='Student ID')
    def student_id_uploaded(self, obj):
        return bool(obj.student_id_image)

    @admin.display(description='Student ID Preview')
    def student_id_preview(self, obj):
        if not obj.student_id_image:
            return 'No student ID uploaded.'
        return format_html('<a href="{}" target="_blank">View uploaded student ID</a>', obj.student_id_image.url)

    @admin.display(description='Payment Message Draft')
    def payment_message_preview(self, obj):
        message = obj.payment_message_draft()
        return format_html('<textarea rows="5" cols="90" readonly>{}</textarea>', message)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'method_type', 'account_label', 'account_value', 'active', 'display_order')
    list_filter = ('method_type', 'active')
    list_editable = ('display_order', 'active')
    search_fields = ('name', 'code', 'account_value')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'talk_title', 'display_order', 'speaker_photo_preview')
    list_editable = ('display_order',)
    search_fields = ('name', 'role', 'talk_title')
    readonly_fields = ('speaker_photo_preview',)

    @admin.display(description='Photo Preview')
    def speaker_photo_preview(self, obj):
        if obj.speaker_photo:
            return format_html('<img src="{}" style="height:80px;border-radius:8px;" />', obj.speaker_photo.url)
        if obj.photo_url:
            return format_html('<img src="{}" style="height:80px;border-radius:8px;" />', obj.photo_url)
        return 'No photo'


@admin.register(TicketTier)
class TicketTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'active', 'is_highlighted')
    list_filter = ('active', 'is_highlighted')
    list_editable = ('price', 'active', 'is_highlighted')


@admin.register(ProgrammeSession)
class ProgrammeSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_type', 'start_time', 'end_time', 'speaker', 'display_order')
    list_filter = ('session_type',)
    list_editable = ('display_order',)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'display_order')
    list_filter = ('active',)
    list_editable = ('display_order',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer_type', 'is_vip_only', 'active', 'display_order')
    list_filter = ('offer_type', 'is_vip_only', 'active')


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent_off', 'active', 'ticket_tier')
    list_filter = ('active',)


admin.site.register(PlaybookLead)
admin.site.register(ClickEvent)
admin.site.register(EmailLog)
