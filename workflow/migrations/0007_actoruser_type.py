# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_auto_20151210_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='actoruser',
            name='type',
            field=models.IntegerField(default=0, choices=[(0, b'\xe5\x9b\xba\xe5\xae\x9a\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba'), (1, b'\xe5\x8a\xa0\xe7\xad\xbe\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba')]),
        ),
    ]
