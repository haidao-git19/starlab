# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0016_auto_20160310_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dev_person',
            field=models.ForeignKey(related_name='dev_person', verbose_name=b'\xe5\xbc\x80\xe5\x8f\x91\xe4\xba\xba\xe5\x91\x98', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='service_department',
            field=models.TextField(max_length=250, null=True, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe6\x89\x80\xe5\xb1\x9e\xe9\x83\xa8\xe9\x97\xa8', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='test_person',
            field=models.ForeignKey(related_name='test_person', verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe4\xba\xba\xe5\x91\x98', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='applyUserId',
            field=models.ForeignKey(related_name='applyUser', verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
        ),
    ]
