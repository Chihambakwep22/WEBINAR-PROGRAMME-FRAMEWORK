from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import DiscountCode, PlaybookLead, Registration, TicketTier


class RegistrationForm(forms.ModelForm):
    discount_code_text = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Registration
        fields = ['full_name', 'email', 'phone_number', 'ticket_tier', 'student_id_image']

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if Registration.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email is already registered for the webinar.')
        return email

    def clean(self):
        cleaned = super().clean()
        tier = cleaned.get('ticket_tier')
        code_text = cleaned.get('discount_code_text', '').strip()

        discount = None
        if code_text:
            try:
                discount = DiscountCode.objects.get(code__iexact=code_text, active=True)
            except DiscountCode.DoesNotExist as exc:
                raise ValidationError({'discount_code_text': 'Invalid discount code.'}) from exc
            if discount.ticket_tier and tier and discount.ticket_tier_id != tier.id:
                raise ValidationError({'discount_code_text': 'This code is not valid for the selected tier.'})

        student_id_image = cleaned.get('student_id_image')
        if tier and tier.code == 'student' and not student_id_image:
            raise ValidationError({'student_id_image': 'Student ID image is required for the Student tier.'})

        if tier:
            final_price = Decimal(tier.price)
            if discount:
                final_price = final_price * Decimal(max(0, 100 - discount.percent_off)) / Decimal(100)
            cleaned['discount_obj'] = discount
            cleaned['computed_final_price'] = final_price.quantize(Decimal('0.01'))

        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.discount_code = self.cleaned_data.get('discount_obj')
        obj.final_price = self.cleaned_data.get('computed_final_price', Decimal('0.00'))
        if commit:
            obj.save()
        return obj


class PlaybookLeadForm(forms.ModelForm):
    class Meta:
        model = PlaybookLead
        fields = ['email']


class RegistrationFilterForm(forms.Form):
    ticket_tier = forms.ModelChoiceField(
        queryset=TicketTier.objects.filter(active=True),
        required=False,
    )
    email = forms.CharField(max_length=120, required=False)
