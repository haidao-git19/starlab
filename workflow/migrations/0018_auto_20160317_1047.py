# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0017_auto_20160310_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dev_person',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\xbc\x80\xe5\x8f\x91\xe4\xba\xba\xe5\x91\x98', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='test_person',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe6\xb5\x8b\xe8\xaf\x95\xe4\xba\xba\xe5\x91\x98', blank=True),
        ),
    ]
