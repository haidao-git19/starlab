__author__ = 'yuan.gao'

from django.conf.urls import include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^category/$', login_required(CategoryListView.as_view()), name='category-list'),
]

# ajax