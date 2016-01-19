# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0005_auto_20160119_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='version',
            field=models.CharField(max_length=5000),
        ),
    ]
