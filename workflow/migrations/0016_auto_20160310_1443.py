# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0015_auto_20160108_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='content',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='itemType',
            field=models.IntegerField(default=0, choices=[(0, b'\xe6\x97\xa5\xe5\xb8\xb8\xe5\x8f\x98\xe6\x9b\xb4'), (1, b'\xe7\xb4\xa7\xe6\x80\xa5\xe5\x8f\x98\xe6\x9b\xb4'), (2, b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8f\x98\xe6\x9b\xb4')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='reason',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe5\x8e\x9f\xe5\x9b\xa0', blank=True),
        ),
    ]
