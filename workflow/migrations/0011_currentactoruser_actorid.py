# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0010_currentactoruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentactoruser',
            name='actorId',
            field=models.ForeignKey(default=1, to='workflow.Actor'),
        ),
    ]
