# coding:utf8
from django.shortcuts import render
from django.views.generic import ListView
from .models import Issues, Projects
# Create your views here.

# Issues models structure
# tracker_id = models.IntegerField()
# project_id = models.IntegerField()
# subject = models.CharField(max_length=255)
# description = models.TextField(blank=True, null=True)
# due_date = models.DateField(blank=True, null=True)
# category_id = models.IntegerField(blank=True, null=True)
# status_id = models.IntegerField()
# assigned_to_id = models.IntegerField(blank=True, null=True)
# priority_id = models.IntegerField()
# fixed_version_id = models.IntegerField(blank=True, null=True)
# author_id = models.IntegerField()
# lock_version = models.IntegerField()
# created_on = models.DateTimeField(blank=True, null=True)
# updated_on = models.DateTimeField(blank=True, null=True)
# start_date = models.DateField(blank=True, null=True)
# done_ratio = models.IntegerField()
# estimated_hours = models.FloatField(blank=True, null=True)
# parent_id = models.IntegerField(blank=True, null=True)
# root_id = models.IntegerField(blank=True, null=True)
# lft = models.IntegerField(blank=True, null=True)
# rgt = models.IntegerField(blank=True, null=True)
# is_private = models.IntegerField()
# closed_on = models.DateTimeField(blank=True, null=True)
import time
from django.shortcuts import get_object_or_404


class EventSubprojectView(ListView):
    template_name = "event/status.html"
    queryset = Issues.objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventSubprojectView, self).get_context_data(**kwargs)
        raw_sql = '''select a.id, a.tracker_id, a.project_id, count(case when a.status_id=5 then a.status_id end) close_count, count(case when a.status_id NOT LIKE 5 then a.status_id end) open_count
                  from issues a GROUP BY project_id;'''
        queryset = Issues.objects.using('eventdb').raw(raw_sql)
        data = []
        for item in queryset:
            if item.project_id not in [15,]:
                project = get_object_or_404(Projects.objects.using('eventdb'), id=item.project_id)
                data.append((project.name, item.open_count, item.close_count))
        open_list = Issues.objects.using('eventdb').raw("SELECT * FROM issues WHERE status_id NOT LIKE 5")
        context['graphTitle'] = "不同子项目的状态"
        context['current_page'] = "event-subproject"
        context['data'] = data
        context['open_list'] = open_list
        context['open'] = True
        return context


class EventTypeView(ListView):
    template_name = "event/status.html"
    queryset = Issues.objects.using('eventdb').all()

    def get_context_data(self, **kwargs):
        context = super(EventTypeView, self).get_context_data(**kwargs)
        context['graphTitle'] = "不同事件类型的状态"
        context['current_page'] = "event-type"
        context['open'] = False
        return context


class EventLevelView(ListView):
    template_name = "event/status.html"
    queryset = Issues.objects.using('eventdb').all()

    def get_context_data(self, **kwargs):
        context = super(EventLevelView, self).get_context_data(**kwargs)
        context['graphTitle'] = "不同事件等级的状态"
        context['current_page'] = "event-level"
        context['open'] = False
        return context




