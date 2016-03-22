from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from .models import *
from .forms import *
from django.shortcuts import render_to_response
# Create your views here.

class HomePageView(TemplateView):
    template_name = "track/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # add your paras
        context["category_list"] = EventCategory.objects.all()
        context["level_list"] = Level.objects.all()
        context["current_page"] = "track-home"
        return context


class EventListView(ListView):
    model = Event
    template_name_suffix = "_list"

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        # add your paras
        context["current_page"] = "track-event-list"
        return context


class EventDetailView(DetailView):
    model = Event
    template_name_suffix = "_detail"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        # add your paras
        context["current_page"] = "track-event-detail"
        return context


class EventCreateView(CreateView):
    form_class = EventForm
    template_name = "track/event_create.html"

    def form_valid(self, form):
        form.instance.offer_people = self.request.user
        return super(EventCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        # add your paras
        context["current_page"] = "track-event-create"
        return context

def event_create(request):
    form = EventForm(initial={
        'offer_people': request.user
    })
    if request.method == "POST":
        pass
    return render_to_response("track/event_create.html", locals())


class EventUpdateView(UpdateView):
    form_class = EventForm
    model = Event
    # fields = '__all__'
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        # add your paras
        context["current_page"] = "track-event-update"
        return context