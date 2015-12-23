# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0013_remove_currentactoruser_actoruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='version',
            field=models.CharField(default='[\u4efb\u52a1\u5f00\u59cb]\n', max_length=500),
        ),
    ]
