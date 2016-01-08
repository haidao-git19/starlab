__author__ = 'yuan.gao'
from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('workorder/order_form.html')
def get_order_form(cat=None):
    #TODO
    return {'cats': Category.objects.all(), 'act_cat': cat}