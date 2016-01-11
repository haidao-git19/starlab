__author__ = 'yuan.gao'
from django import template
from workorder.forms import OrderForm
import time
register = template.Library()

@register.inclusion_tag('workorder/order_form.html')
def get_order_form(request=None):
    name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    form = OrderForm(
        initial={
            'name': name,
            'owner': request.user,
            'state': 0,
        }
    )
    return {'form': form}