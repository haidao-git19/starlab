# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_auto_20151207_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'ordering': ['routId'], 'verbose_name': '\u6b65\u9aa4', 'verbose_name_plural': '\u6b65\u9aa4'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': '\u5de5\u5355', 'verbose_name_plural': '\u5de5\u5355'},
        ),
        migrations.AddField(
            model_name='actoruser',
            name='state',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='item',
            name='comment',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='content',
            field=models.CharField(max_length=50, null=True, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='incidence',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xbd\xb1\xe5\x93\x8d\xe8\x8c\x83\xe5\x9b\xb4', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='operation',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\x85\xb7\xe4\xbd\x93\xe6\x93\x8d\xe4\xbd\x9c', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='reason',
            field=models.CharField(max_length=50, null=True, verbose_name=b'\xe5\x8e\x9f\xe5\x9b\xa0', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='rollback',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\x9b\x9e\xe6\xbb\x9a', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 8, 1, 42, 55, 132089, tzinfo=utc), verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='actor',
            name='sortNo',
            field=models.IntegerField(verbose_name=b'\xe6\xad\xa5\xe9\xaa\xa4\xe7\xbc\x96\xe5\x8f\xb7(\xe4\xbb\x8e1\xe5\xbc\x80\xe5\xa7\x8b)'),
        ),
        migrations.AlterField(
            model_name='item',
            name='applyUserId',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='routID',
            field=models.ForeignKey(verbose_name=b'\xe4\xbd\xbf\xe7\x94\xa8\xe6\xb5\x81\xe7\xa8\x8b', to='workflow.Rout'),
        ),
        migrations.AlterField(
            model_name='rout',
            name='state',
            field=models.IntegerField(choices=[(0, b'\xe8\x8d\x89\xe7\xa8\xbf'), (1, b'\xe5\xb7\xb2\xe5\x8f\x91\xe5\xb8\x83'), (2, b'\xe5\x81\x9c\xe6\xad\xa2')]),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='actorId',
            field=models.ForeignKey(verbose_name=b'\xe6\xad\xa5\xe9\xaa\xa4', to='workflow.Actor'),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='itemId',
            field=models.ForeignKey(verbose_name=b'\xe5\xb7\xa5\xe5\x8d\x95', to='workflow.Item'),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='state',
            field=models.IntegerField(default=1, choices=[(0, b'\xe6\xa3\x80\xe5\x87\xba'), (1, b'\xe5\xbe\x85\xe6\xa3\x80\xe5\x87\xba')]),
        ),
    ]
