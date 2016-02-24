__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', AmapIndexView.as_view(), name='index'),
]

# ajax
urlpatterns += [
    url('^get_all_points/$', get_all_points, name="get_all_points"),
]