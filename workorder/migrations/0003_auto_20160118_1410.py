# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0002_auto_20160108_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 18, 14, 10, 16, 605849), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='category2',
            field=models.ForeignKey(related_name='ordercategory2', verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', to='workorder.Category2'),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'\xe5\xb7\xa5\xe5\x8d\x95\xe7\xbc\x96\xe5\x8f\xb7'),
        ),
        migrations.AlterField(
            model_name='order',
            name='rout',
            field=models.ForeignKey(related_name='orderrout', default=1, to='workorder.Rout'),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xbe\x85\xe5\x88\x9b\xe5\xbb\xba\xe4\xbb\xbb\xe5\x8a\xa1'), (1, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\x9e\xe6\x96\xbd\xe4\xb8\xad'), (3, b'\xe5\xb7\xa5\xe5\x8d\x95\xe5\xb7\xb2\xe5\x85\xb3\xe9\x97\xad')]),
        ),
    ]
