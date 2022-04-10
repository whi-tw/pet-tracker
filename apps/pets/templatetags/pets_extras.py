from django import template
from django.utils import timezone
import arrow

register = template.Library()


@register.filter
def addstr(arg1, arg2) -> str:
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def humanizetime(arg1) -> str:
    arg1 = arrow.get(arg1)
    before = arrow.get(timezone.now()).shift(months=-1).datetime
    if arg1 < before:
        return arg1.datetime.time()
    else:
        return arg1.humanize()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()
