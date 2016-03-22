__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(HomePageView.as_view()), name='home'),
    url(r'^event_list$', login_required(EventListView.as_view()), name='event_list'),
    url(r'^event_list_over$', login_required(EventOverView.as_view()), name='event_list_over'),
    url(r'^event_list_my$', login_required(EventMyView.as_view()), name='event_list_my'),
    url(r'^event_detail/(?P<pk>[0-9]+)/$', login_required(EventDetailView.as_view()), name='event-detail'),
    url(r'^event_create$', login_required(EventCreateView.as_view()), name='event-create'),
    url(r'^event_update/(?P<pk>[0-9]+)/$', login_required(EventUpdateView.as_view()), name='event-update'),
]

# ajax

urlpatterns += [
    url(r'^event_end', event_end, name='event-end'),
]