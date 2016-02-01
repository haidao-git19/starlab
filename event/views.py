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
import datetime
from django.shortcuts import get_object_or_404
import json


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


class WeeklyEventView(ListView):
    template_name = "event/weekly.html"
    queryset = Issues.objects.using('eventdb').all()

    def get_context_data(self, **kwargs):
        context = super(WeeklyEventView, self).get_context_data(**kwargs)
        context['graphTitle'] = "七天事件处理趋势图(线性图)"
        context['current_page'] = "event-weekly"
        project_list = ['基站','网络','系统','应用(开放平台)','应用(数据算法)']
        today_date = datetime.date.today()
        date_list = [
            today_date - datetime.timedelta(days = 7),
            today_date - datetime.timedelta(days = 6),
            today_date - datetime.timedelta(days = 5),
            today_date - datetime.timedelta(days = 4),
            today_date - datetime.timedelta(days = 3),
            today_date - datetime.timedelta(days = 2),
            today_date - datetime.timedelta(days = 1),
         ]
        weekly = []
        for i in date_list:
            weekly.append("{}月{}日".format(i.month, i.day))
        project_dict = {
            "基站": 16,
            "网络": 14,
            "系统": 13,
            "应用(开放平台)": 17,
            "应用(数据算法)": 18,
        }
        tmp_querysets = Issues.objects.using('eventdb').filter(created_on__gt=datetime.datetime.now()-datetime.timedelta(days = 7))
        print tmp_querysets
        counts_list = []
        for project in project_list:
            a = []
            for date in date_list:
                b = 0
                for i in tmp_querysets.filter(project_id=project_dict[project]):
                    if i.created_on.month == date.month and i .created_on.day == date.day:
                        b += 1
                a.append(b)
            counts_list.append(a)
        context['counts_list'] = json.dumps(counts_list)
        context['weekly'] = json.dumps(weekly) # x轴
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




