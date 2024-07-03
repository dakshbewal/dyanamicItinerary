# custom_filters.py
from django import template
from itertools import zip_longest

register = template.Library()

@register.filter
def zip_longest_list(a, b):
    return zip_longest(a, b)