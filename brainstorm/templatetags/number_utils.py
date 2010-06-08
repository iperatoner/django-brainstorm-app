from django import template

register = template.Library()

@register.filter('put_zero_before')
def put_zero_before(value):
    value = str(value)
    
    if len(value) < 2:
        value = '0' + value
    
    return value
