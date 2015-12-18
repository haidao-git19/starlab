__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^sub-project', EventSubprojectView.as_view(), name='sub-project'),
    url(r'^type$', EventTypeView.as_view(), name='type'),
    url(r'^level', EventLevelView.as_view(), name='level'),
]