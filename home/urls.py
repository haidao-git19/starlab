__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import HomePageView, track_url

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index'),
    url(r'^goto/$', track_url, name='goto'),
]