from django.shortcuts import render
from django.views.generic import ListView
from home.models import Website
from .models import Receiver
from django.core import serializers
# Create your views here.


class AmapIndexView(ListView):
    template_name = "amap/index.html"
    queryset = Receiver.objects.using('stationdb').none()

    def get_context_data(self, **kwargs):
        context = super(AmapIndexView, self).get_context_data(**kwargs)
        querysets = Receiver.objects.using('stationdb').filter(enabled=1)
        data = serializers.serialize('json', querysets, fields=(
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