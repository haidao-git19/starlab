# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0008_category2_auto_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category2',
            name='auto_template',
            field=models.TextField(max_length=5000, null=True, blank=True),
        ),
    ]
