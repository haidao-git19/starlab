# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0010_proposermanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='purpose',
            field=models.TextField(max_length=5000, null=True, verbose_name=b'\xe7\x9b\xae\xe7\x9a\x84', blank=True),
        ),
    ]
