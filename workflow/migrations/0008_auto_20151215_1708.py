# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0007_actoruser_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-start_time'], 'verbose_name': '\u5de5\u5355', 'verbose_name_plural': '\u5de5\u5355'},
        ),
        migrations.AlterModelOptions(
            name='tasklist',
            options={'ordering': ['itemId'], 'verbose_name': '\u4efb\u52a1\u5217\u8868', 'verbose_name_plural': '\u4efb\u52a1\u5217\u8868'},
        ),
        migrations.AlterField(
            model_name='changeapply',
            name='add_sign',
            field=models.ManyToManyField(related_name='signer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
    ]
