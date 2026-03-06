from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_um(value):
    """Format price in Ouguiya (UM) with thousands separator"""
    if value is None:
        return "0,00 UM"
    
    try:
        value = Decimal(str(value))
        # Format with 2 decimal places and comma thousands separator
        formatted = f"{value:,.2f}".replace(',', '|').replace('.', ',').replace('|', ',')
        return f"{formatted} UM"
    except:
        return f"{value} UM"
