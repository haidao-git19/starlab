# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0012_auto_20151222_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentactoruser',
            name='actorUser',
        ),
    ]
