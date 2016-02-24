# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0011_auto_20160222_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='version',
            field=models.TextField(max_length=5000),
        ),
    ]
