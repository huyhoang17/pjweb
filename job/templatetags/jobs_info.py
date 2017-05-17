from django import template

register = template.Library()


@register.filter(is_safe=True)
def dot_replace(value):
    value = value.replace('|', '. ')
    return value
