# In your app's templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_by_index(queryset, index):
    return queryset[index - 1]