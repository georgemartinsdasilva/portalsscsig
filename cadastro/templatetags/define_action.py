from django import template
from django.template.defaultfilters import stringfilter
import base64
register = template.Library()


@register.filter
@stringfilter
def trim(value):
    return value.strip()


@register.filter
@stringfilter
def encoder(value):
    if value == None:
        pass
    else:
        a = base64.b64encode(bytes(value, "utf-8"))
        b = base64.b64encode(bytes(a.decode('utf-8'), "utf-8"))
        c = base64.b64encode(bytes(b.decode('utf-8'), "utf-8"))
    return c.decode('utf-8')


