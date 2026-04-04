from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def split_lines(value):
    if not value:
        return []
    return [line.strip() for line in str(value).splitlines() if line.strip()]


@register.filter
def get_item(mapping, key):
    if not mapping:
        return None
    return mapping.get(key)


@register.filter
def convert_currency(amount, currency):
    if amount is None:
        return Decimal('0.00')

    value = Decimal(str(amount))
    if currency == 'ZAR':
        return value * Decimal('15')
    return value
