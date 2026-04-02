from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import PlaybookLeadForm, RegistrationForm
from .models import ClickEvent, Offer, ProgrammeSession, Registration, Speaker, Sponsor, TicketTier
from .services import send_registration_confirmation


def global_context():
    return {
        'event_title': 'From Zero to Momentum: Mastering Personal Development & Entrepreneurship the African Way',
        'event_hosts': 'Quantilytix x Impactpreneur Global',
        'event_datetime': 'April 22, 2026 | 7:00 PM GST / 8:00 PM WAT',
        'event_start_iso': settings.EVENT_START_ISO,
        'sponsors': Sponsor.objects.filter(active=True),
    }


def home(request):
    context = {
        **global_context(),
        'tiers': TicketTier.objects.filter(active=True),
        'speaker_count': Speaker.objects.count(),
    }
    return render(request, 'core/index.html', context)


def speakers(request):
    speaker_images = {
        'George Bassey': static('speakers/GeorgeBassey.png'),
        'Helper Zhou': static('speakers/HelperZhou.png'),
        'Quantilytix Team': static('speakers/HelperZhou.png'),
    }
    context = {
        **global_context(),
        'speakers': Speaker.objects.all(),
        'speaker_images': speaker_images,
    }
    return render(request, 'core/speakers.html', context)


def programme(request):
    context = {**global_context(), 'sessions': ProgrammeSession.objects.select_related('speaker')}
    return render(request, 'core/programme.html', context)


def pricing(request):
    context = {**global_context(), 'tiers': TicketTier.objects.filter(active=True)}
    return render(request, 'core/pricing.html', context)


def sponsors(request):
    context = {**global_context(), 'sponsors': Sponsor.objects.filter(active=True)}
    return render(request, 'core/sponsors.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save()
            send_registration_confirmation(reg)
            messages.success(request, 'Registration successful. Confirmation email has been sent.')
            return redirect('registration_success', registration_id=reg.id)
    else:
        form = RegistrationForm()

    context = {
        **global_context(),
        'form': form,
        'tiers': TicketTier.objects.filter(active=True),
    }
    return render(request, 'core/register.html', context)


def registration_success(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    return render(
        request,
        'core/registration_success.html',
        {**global_context(), 'registration': registration},
    )


def offers(request):
    reg_id = request.GET.get('registration')
    registration = None
    if reg_id and reg_id.isdigit():
        registration = Registration.objects.filter(id=int(reg_id)).first()

    queryset = Offer.objects.filter(active=True)
    if registration and registration.ticket_tier.name.lower() != 'vip':
        queryset = queryset.filter(is_vip_only=False)

    playbook_form = PlaybookLeadForm()
    context = {
        **global_context(),
        'offers': queryset,
        'registration': registration,
        'playbook_form': playbook_form,
    }
    return render(request, 'core/offers.html', context)


@require_POST
def capture_playbook_lead(request):
    form = PlaybookLeadForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Playbook access link will be sent to your email.')
    else:
        messages.error(request, 'Please enter a valid email. If you already subscribed, use another email.')
    return redirect('offers')


@require_POST
def track_click(request):
    event_type = request.POST.get('event_type', '').strip()[:50]
    cta_url = request.POST.get('cta_url', '')
    reg_id = request.POST.get('registration_id', '')

    registration = None
    if reg_id.isdigit():
        registration = Registration.objects.filter(id=int(reg_id)).first()

    ClickEvent.objects.create(
        event_type=event_type or 'unknown',
        session_key=request.session.session_key or '',
        registration=registration,
        metadata={'cta_url': cta_url, 'timestamp': datetime.utcnow().isoformat()},
    )

    return JsonResponse({'ok': True})


@staff_member_required
def registration_dashboard(request):
    queryset = Registration.objects.select_related('ticket_tier').all()

    tier = request.GET.get('tier', '').strip()
    email = request.GET.get('email', '').strip()
    if tier.isdigit():
        queryset = queryset.filter(ticket_tier_id=int(tier))
    if email:
        queryset = queryset.filter(email__icontains=email)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
        response.write('Name,Email,Phone,Tier,Final Price,Paid,Attended,Created At\n')
        for item in queryset:
            response.write(
                f'"{item.full_name}","{item.email}","{item.phone_number}","{item.ticket_tier.name}",'
                f'"{item.final_price}","{item.payment_confirmed}","{item.attended}","{timezone.localtime(item.created_at)}"\n'
            )
        return response

    page = Paginator(queryset, 25).get_page(request.GET.get('page'))
    tier_counts = Registration.objects.values('ticket_tier__name').annotate(total=Count('id'))

    context = {
        **global_context(),
        'page': page,
        'ticket_tiers': TicketTier.objects.filter(active=True),
        'selected_tier': tier,
        'email_query': email,
        'tier_counts': tier_counts,
        'total_registrations': Registration.objects.count(),
        'event_start': settings.EVENT_START_ISO,
    }
    return render(request, 'core/dashboard.html', context)
