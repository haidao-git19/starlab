__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^sub-project', EventSubprojectView.as_view(), name='sub-project'),
    url(r'^weekly$', WeeklyEventView.as_view(), name='weekly'),
    url(r'^weekly-percent$', WeeklyEventPercentView.as_view(), name='weekly-percent'),
    url(r'^weekly-type-count', WeeklyEventTypeView.as_view(), name='weekly-type-count'),
]