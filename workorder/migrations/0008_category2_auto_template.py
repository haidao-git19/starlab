# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0007_auto_20160127_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='category2',
            name='auto_template',
            field=models.CharField(max_length=5000, null=True, blank=True),
        ),
    ]
