# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category1',
            options={'ordering': ['id'], 'verbose_name': '\u5927\u7c7b', 'verbose_name_plural': '\u5927\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='category2',
            options={'ordering': ['category1', 'id'], 'verbose_name': '\u5c0f\u7c7b', 'verbose_name_plural': '\u5c0f\u7c7b'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='category1',
        ),
        migrations.AlterField(
            model_name='category2',
            name='category1',
            field=models.ForeignKey(related_name='category', to='workorder.Category1'),
        ),
    ]
