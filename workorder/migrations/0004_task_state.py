# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0003_auto_20160118_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='state',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe6\x96\xb0\xe5\x88\x9b\xe5\xbb\xba\xe4\xbb\xbb\xe5\x8a\xa1'), (1, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\x9e\xe6\x96\xbd\xe4\xb8\xad'), (3, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f')]),
        ),
    ]
