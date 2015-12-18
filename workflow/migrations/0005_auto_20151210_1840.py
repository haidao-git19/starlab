# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0004_auto_20151208_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='comment',
            field=models.CharField(max_length=5000, null=True, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='incidence',
            field=models.CharField(max_length=5000, null=True, verbose_name=b'\xe5\xbd\xb1\xe5\x93\x8d\xe8\x8c\x83\xe5\x9b\xb4', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='itemType',
            field=models.IntegerField(default=0, choices=[(0, b'\xe5\xb8\xb8\xe8\xa7\x84\xe5\x8f\x98\xe6\x9b\xb4'), (1, b'\xe7\xb4\xa7\xe6\x80\xa5\xe5\x8f\x98\xe6\x9b\xb4')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='operation',
            field=models.CharField(max_length=5000, null=True, verbose_name=b'\xe5\x85\xb7\xe4\xbd\x93\xe6\x93\x8d\xe4\xbd\x9c', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='rollback',
            field=models.CharField(max_length=5000, null=True, verbose_name=b'\xe5\x9b\x9e\xe6\xbb\x9a', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='state',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x89\x88\xe6\x9c\xac\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe5\xbe\x85\xe5\xae\xa1\xe6\x89\xb9'), (1, b'\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe5\xb7\xb2\xe5\x85\xb3\xe9\x97\xad')]),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='state',
            field=models.IntegerField(default=1, choices=[(0, b'\xe6\xa3\x80\xe5\x87\xba'), (1, b'\xe7\xbb\x93\xe6\x9d\x9f')]),
        ),
    ]
