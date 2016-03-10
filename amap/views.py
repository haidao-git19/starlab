# coding:utf8
from django.shortcuts import render
from django.views.generic import ListView
from home.models import Website
from .models import Receiver
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render_to_response, HttpResponse
# Create your views here.


class AmapIndexView(ListView):
    template_name = "amap/index.html"
    queryset = Receiver.objects.using('stationdb').none()

    def get_context_data(self, **kwargs):
        context = super(AmapIndexView, self).get_context_data(**kwargs)
        querysets = Receiver.objects.using('stationdb').filter(enabled=1)
        data = serializers.serialize('json', querysets, fields=(
            'id',
            'state',
            'latitude',
            'longitude',
            'category_id',
            'rec_sn',
            'station_cnname',
            'station_ip',
            'sat_num',
            'ant_angle',
            'real_time',
            'station_code',
            'rec_type',
            'device_type',
            'station_pm',
            'station_agent_owner',
            'station_agent_contact',
            'station_industry',
            ),
        )
        context['data'] = data
        context['num'] = querysets.count()
        context['num1'] = querysets.filter(category_id=1, state=1).count()
        context['num2'] = querysets.filter(category_id=1, state=0).count()
        context['num3'] = querysets.filter(category_id=2, state=1).count()
        context['num4'] = querysets.filter(category_id=2, state=0).count()
        context['num5'] = querysets.filter(category_id=3, state=1).count()
        context['num6'] = querysets.filter(category_id=3, state=0).count()

        context['current_page'] = "amap-index"
        return context

@csrf_exempt
def get_all_points(request):
    querysets = Receiver.objects.using('stationdb').filter(enabled=1)
    data = serializers.serialize('json', querysets, fields=(
        'id',
        'state',
        'latitude',
        'longitude',
        'category_id',
        'rec_sn',
        'station_cnname',
        'station_ip',
        'sat_num',
        'ant_angle',
        'real_time',
        'station_code',
        'rec_type',
        'device_type',
        'station_pm',
        'station_agent_owner',
        'station_agent_contact',
        'station_industry',
        ),
    )
    return JsonResponse(data, status=200, safe=False)

@csrf_exempt
def get_xxx_points(request):
    category_no = request.POST.get('category_no')
    list = str(category_no).split(',')
    tl = []
    for i in list:
        tl.append((i[2:3], i[3:4]))
    querysets = Receiver.objects.using('stationdb').filter(enabled=1)
    querysets_result = Receiver.objects.none()
    for (i, j) in tl:
        querysets_result = querysets.filter(category_id=i, state=j) | querysets_result
        print querysets_result.count()
    data = serializers.serialize('json', querysets_result, fields=(
        'id',
        'state',
        'latitude',
        'longitude',
        'category_id',
        'rec_sn',
        'station_cnname',
        'station_ip',
        'sat_num',
        'ant_angle',
        'real_time',
        'station_code',
        'rec_type',
        'device_type',
        'station_pm',
        'station_agent_owner',
        'station_agent_contact',
        'station_industry',
        ),
    )
    return JsonResponse(data, status=200, safe=False)


def station_detail(request):
    station_id = request.GET.get('pk', '')
    # return render_to_response(station_id)
    return HttpResponse("基站ID:{}<br>图片:http://127.0.0.1:8000/static/img/{}".format(station_id, station_id))