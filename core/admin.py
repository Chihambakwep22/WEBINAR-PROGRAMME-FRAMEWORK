from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook

from .models import (
    ClickEvent,
    DiscountCode,
    EmailLog,
    Offer,
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
    ws.append(['Name', 'Email', 'Phone', 'Tier', 'Final Price', 'Paid', 'Attended', 'Created'])

    for row in queryset.select_related('ticket_tier'):
        ws.append(
            [
                row.full_name,
                row.email,
                row.phone_number,
                row.ticket_tier.name,
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
        'final_price',
        'payment_confirmed',
        'attended',
        'created_at',
    )
    list_filter = ('ticket_tier', 'payment_confirmed', 'attended', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    actions = [export_to_excel]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'talk_title', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('name', 'role', 'talk_title')


@admin.register(TicketTier)
class TicketTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'active', 'is_highlighted')
    list_filter = ('active', 'is_highlighted')


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
