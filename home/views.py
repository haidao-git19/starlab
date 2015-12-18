from django.shortcuts import render
from django.views.generic import ListView
from .models import Website

# Create your views here.


class HomePageView(ListView):
    queryset = Website.objects.all()
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['row'] = "1-4"
        context['current_page'] = "home-index"
        return context
