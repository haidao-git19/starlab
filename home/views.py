from django.shortcuts import render
from django.views.generic import ListView
from .models import Website
from django.shortcuts import redirect

# Create your views here.


class HomePageView(ListView):
    queryset = Website.objects.all()
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['row'] = "1-4"
        context['current_page'] = "home-index"
        return context



def track_url(request):
    page_id = None
    url = '/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Website.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)