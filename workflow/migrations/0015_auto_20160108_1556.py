# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0014_auto_20151223_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currentactoruser',
            options={'verbose_name': '\u4e34\u65f6\u6b65\u9aa4\u5904\u7406\u4eba', 'verbose_name_plural': '\u4e34\u65f6\u6b65\u9aa4\u5904\u7406\u4eba'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-start_time'], 'verbose_name': '\u53d8\u66f4', 'verbose_name_plural': '\u53d8\u66f4'},
        ),
    ]
