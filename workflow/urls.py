__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^items/$', login_required(ItemListView.as_view()), name='item-list'),
    url(r'^item_create/$', itemcreate, name='item-create'),
    url(r'^item_update/(?P<pk>[-\w]+)/$', ItemUpdateView.as_view(), name='item-update'),
    url(r'^item_detail/(?P<pk>[-\w]+)/$', ItemDetailView.as_view(), name='item-detail'),
    # url(r'^itemcreate/$', ItemCreateView.as_view(), name='item-create'),
    url(r'^tasks/$', TaskListView.as_view(), name='task-list'),
    url(r'^actorUser/$', login_required(GetActorUserFromTask.as_view()), name='actoruser-list'),
]


# ajax
urlpatterns += [
    url(r'^createTask/$', createTask, name='create-task'),
    url(r'^agree/$', agree, name='agree'),
    url(r'^disagree/$', disagree, name='disagree'),
    url(r'^add_sign/$', add_sign, name='add_sign'),
]