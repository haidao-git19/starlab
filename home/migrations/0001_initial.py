# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('order', models.IntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('img', models.ImageField(upload_to=b'img', verbose_name='\u914d\u56fe(\u6ce8\u610f\u6bd4\u4f8b)')),
                ('description', models.CharField(max_length=100, verbose_name='\u63cf\u8ff0')),
                ('owner', models.ForeignKey(verbose_name='\u7ba1\u7406\u5458', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u89c2\u661f\u53f0',
                'verbose_name_plural': '\u89c2\u661f\u53f0',
            },
        ),
    ]
