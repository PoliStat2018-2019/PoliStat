from django import template

register = template.Library()

@register.filter
def percentage(value):
    return format(value, ".1%")

@register.filter
def pretty_percentage(value):
    if value < 0.05:
        return "near 0%"
    elif value > 0.95:
        return "near 100%"
    return format(value, ".1%")