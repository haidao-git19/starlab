__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^category/$', CategoryListView.as_view(), name='category-list'),
    url(r'^create_order/$', login_required(OrderCreateView.as_view()), name='order-create'),
    url(r'^list_order_user/$', login_required(OrderOfUserListView.as_view()), name='order-list-user'),
    url(r'^list_order_engineer/$', login_required(OrderOfEngineerListView.as_view()), name='order-list-engineer'),
    url(r'^createTask/$', createTask, name='create-task'),
]

# ajax