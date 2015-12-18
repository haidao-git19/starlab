# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0008_auto_20151215_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasklist',
            options={'ordering': ['-id'], 'verbose_name': '\u4efb\u52a1\u5217\u8868', 'verbose_name_plural': '\u4efb\u52a1\u5217\u8868'},
        ),
    ]
