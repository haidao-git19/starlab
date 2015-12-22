# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0011_currentactoruser_actorid'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentactoruser',
            name='comment',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='currentactoruser',
            name='actorId',
            field=models.ForeignKey(to='workflow.Actor'),
        ),
    ]
