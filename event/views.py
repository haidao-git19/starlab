# coding:utf8
from django.shortcuts import render
from django.views.generic import ListView
from .models import Issues, Projects, CustomValues
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

PROJECT_DICT = {
    "基站": 16,
    "网络": 14,
    "系统": 13,
    "应用(开放平台)": 17,
    "应用(数据算法)": 18,
}

class WeeklyEventView(ListView):
    template_name = "event/weekly_created_count.html"
    queryset = Issues.objects.using('eventdb').all()

    def get_context_data(self, **kwargs):
        context = super(WeeklyEventView, self).get_context_data(**kwargs)
        context['graphTitle'] = "七天事件处理趋势图(折线图)"
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
        tmp_querysets = Issues.objects.using('eventdb').filter(created_on__gt=datetime.datetime.now()-datetime.timedelta(days = 7))
        counts_list = []
        for project in project_list:
            a = []
            for date in date_list:
                b = 0
                for i in tmp_querysets.filter(project_id=PROJECT_DICT[project]):
                    if i.created_on.month == date.month and i .created_on.day == date.day:
                        b += 1
                a.append(b)
            counts_list.append(a)
        context['counts_list'] = json.dumps(counts_list)
        context['weekly'] = json.dumps(weekly) # x轴
        return context


class WeeklyEventPercentView(ListView):
    template_name = "event/weekly_percent.html"
    queryset = Issues.objects.using('eventdb').all()

    def get_context_data(self, **kwargs):
        context = super(WeeklyEventPercentView, self).get_context_data(**kwargs)
        context['graphTitle'] = "饼图"
        context['current_page'] = "event-weekly-percent"
        context['open'] = False
        priority_id_dict = {
            1: 'S1',
            2: 'S2',
            3: 'S3',
            5: '无影响',
        }
        priority_id_list = [1, 2, 3, 5]
        tmp_querysets = Issues.objects.using('eventdb').filter(created_on__gt=datetime.datetime.now()-datetime.timedelta(days = 7))
        querysets_by_project = []

        # 过滤项目
        # TODO
        # for i in PROJECT_DICT:
        #     querysets_by_project.append(tmp_querysets.filter(project_id=PROJECT_DICT[i]).count())
        # print querysets_by_project
        # 忽略项目,直接等级
        result_dict = []
        for i in priority_id_dict:
            tmp_count = tmp_querysets.filter(priority_id=i).count()
            result_dict.append({ 'value':tmp_count, 'name':priority_id_dict[i]})
        context['result'] = json.dumps(result_dict)
        context['priority'] = json.dumps(['S1', 'S2', 'S3', '无影响'])
        return context


class WeeklyEventTypeView(ListView):
    template_name = "event/weekly_event_type_count.html"
    queryset = Issues.objects.using('eventdb').all()

    def get_context_data(self, **kwargs):
        context = super(WeeklyEventTypeView, self).get_context_data(**kwargs)
        context['graphTitle'] = "饼图"
        context['current_page'] = "event-weekly-type-count"
        seven_querysets = Issues.objects.using('eventdb').filter(created_on__gt=datetime.datetime.now()-datetime.timedelta(days = 7))
        issues_id_list = seven_querysets.values_list('id', flat=True)
        tmp_querysets = CustomValues.objects.using('eventdb').filter(custom_field_id=6)
        # 类型列表
        type_list = tmp_querysets.values_list('value', flat=True).distinct()
        type_list = list(type_list)
        result_list = []
        for tl in type_list:
            result_list.append(tmp_querysets.filter(value=tl).filter(customized_id__in=issues_id_list).count())
        context['result_list'] = json.dumps(result_list)
        context['type_list'] = json.dumps(type_list)
        return context
