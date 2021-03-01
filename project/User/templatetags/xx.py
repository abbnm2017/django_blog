from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag()
def my_simple_time(v1,v2,v3):
    return v1 + v2 + v3

@register.simple_tag()
def my_input(id,arg):
    result = "<input type='text' id='%s' class='%s'/>"%(id,arg)
    # result = "<script>alert(333)</script>"
    result = mark_safe(result)
    return result

@register.filter()
def my_filter(a,b):

    return a + b


@register.filter()
def mybool(value):
    if value == "gaoda1":
        return True
    return False