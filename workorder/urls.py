__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^category/$', login_required(CategoryListView.as_view()), name='category-list'),
    url(r'^create_order/$', login_required(OrderCreateView.as_view()), name='order-create'),
    url(r'^list_order_user/$', login_required(OrderOfUserListView.as_view()), name='order-list-user'),
    url(r'^list_order_engineer/$', login_required(OrderOfEngineerListView.as_view()), name='order-list-engineer'),
    url(r'^list_task/$', login_required(TaskListView.as_view()), name='list-task'),
    url(r'^list_task_engineer/$', login_required(TaskListEngineerView.as_view()), name='list-task-engineer'),
]

# ajax
urlpatterns += [
    url(r'^createTask/$', createTask, name='create-task'),
    url(r'^dispense/$', dispense, name='dispense-task'),
    url(r'^complete/$', complete, name='complete-task'),
    url(r'^agree/$', agree, name='agree-task'),
    url(r'^auto_template/$', autoComplete, name='auto_complete'),
]