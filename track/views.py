# coding:utf8
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from .models import *
from .forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


class EventOverView(ListView):
    model = Event
    template_name = "track/event_list_over.html"

    def get_context_data(self, **kwargs):
        context = super(EventOverView, self).get_context_data(**kwargs)
        statu = get_object_or_404(EventStatus, name="已办")
        categories = EventCategory.objects.filter(owner=self.request.user)
        context['event_over'] = Event.objects.filter(Q(status=statu) & Q(category__in=categories))
        context['current_page'] = "track-event-over"
        return context


class EventMyView(ListView):
    model = Event
    template_name = "track/event_list_my.html"

    def get_context_data(self, **kwargs):
        context = super(EventMyView, self).get_context_data(**kwargs)
        statu = get_object_or_404(EventStatus, name="待办")
        categories = EventCategory.objects.filter(owner=self.request.user)
        context['event_my'] = Event.objects.filter(Q(status=statu) & Q(category__in=categories))
        context['current_page'] = "track-event-my"
        return context


from DingDing import DingDing
# ajax
@csrf_exempt
def event_end(request):
    id = request.POST.get('id')
    event = get_object_or_404(Event, id=id)
    statu = get_object_or_404(EventStatus, name="已办")
    event.status = statu
    data = {
        'return': "已通知提单人{}".format(event.offer_people)
    }
    # 通知
    dd = DingDing()
    id = event.offer_people.username
    url = request.build_absolute_uri(reverse('track:event_list'))
    jsonmsg = {
        "title": "你提的事件单状态变为已办",
        "text": "{}\n事件ID:{}".format(event.name, event.id),
        "picUrl": "@lALOACZwe2Rk",
        "messageUrl": url,
    }
    dd.send_link_message(ddID=id, json_content=jsonmsg)
    event.save()
    return JsonResponse(data, safe=False)