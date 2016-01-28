# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0006_auto_20160119_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-state'], 'verbose_name': '\u5de5\u5355', 'verbose_name_plural': '\u5de5\u5355'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['state'], 'verbose_name': '\u4efb\u52a1', 'verbose_name_plural': '\u4efb\u52a1'},
        ),
        migrations.AddField(
            model_name='currentactoruser',
            name='state',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xbe\x85\xe5\x88\x9b\xe5\xbb\xba\xe4\xbb\xbb\xe5\x8a\xa1'), (1, b'\xe5\xb7\xa5\xe5\x8d\x95\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe5\xb7\xa5\xe5\x8d\x95\xe5\x88\x86\xe5\x8f\x91\xe4\xb8\xad'), (3, b'\xe5\xb7\xa5\xe5\x8d\x95\xe5\xae\x9e\xe6\x96\xbd\xe4\xb8\xad'), (4, b'\xe5\xb7\xa5\xe5\x8d\x95\xe5\xb7\xb2\xe5\x85\xb3\xe9\x97\xad')]),
        ),
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe6\x96\xb0\xe5\x88\x9b\xe5\xbb\xba\xe4\xbb\xbb\xe5\x8a\xa1'), (1, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x86\xe5\x8f\x91\xe4\xb8\xad'), (3, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\x9e\xe6\x96\xbd\xe4\xb8\xad'), (4, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f')]),
        ),
    ]
