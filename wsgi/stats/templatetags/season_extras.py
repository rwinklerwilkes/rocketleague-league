from django import template
from collections import OrderedDict

register = template.Library()

@register.filter
def dict_sort(value):
    if isinstance(value,dict):
      new_dict = OrderedDict()
      key_list = sorted(value.keys())
      for key in key_list:
        new_dict[key] = value[key]
      return new_dict
    elif isinstance(value,list):
      return sorted(value)
    else:
      return value

@register.filter
def key_sort(value):
    if isinstance(value,dict):
      key_list = sorted(value.keys())
      return key_list
    elif isinstance(value,list):
      return sorted(value)
    else:
      return value
