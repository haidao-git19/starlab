# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='changeapply',
            name='gopass',
            field=models.NullBooleanField(default=None),
        ),
    ]
