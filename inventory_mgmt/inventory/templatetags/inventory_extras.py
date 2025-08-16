from django import template
register = template.Library()

@register.filter
def mul(a, b):
    try:
        return float(a) * float(b)
    except Exception:
        return 0
