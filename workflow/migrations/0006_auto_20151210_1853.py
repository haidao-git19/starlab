# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0005_auto_20151210_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='comment',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='incidence',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe5\xbd\xb1\xe5\x93\x8d\xe8\x8c\x83\xe5\x9b\xb4', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='operation',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe5\x85\xb7\xe4\xbd\x93\xe6\x93\x8d\xe4\xbd\x9c', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='rollback',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe5\x9b\x9e\xe6\xbb\x9a', blank=True),
        ),
    ]
