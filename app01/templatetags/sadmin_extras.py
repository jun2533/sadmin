from django import template


register = template.Library()

@register.filter(name='max')
def get_max(*k):
    return max(*k)

@register.filter(name='test')
def test_filter(value,arg=None):
    return max(value)