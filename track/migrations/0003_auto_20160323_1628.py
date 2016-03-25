# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_auto_20160323_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='comment',
            field=models.CharField(default=None, max_length=5000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='current_people',
            field=models.ForeignKey(related_name='current_people', verbose_name='\u5f53\u524d\u8d23\u4efb\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='desc',
            field=models.CharField(max_length=5000, null=True, blank=True),
        ),
    ]
