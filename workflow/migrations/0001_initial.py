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
            name='ChangeApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('incidence', models.CharField(max_length=255)),
                ('operation', models.CharField(max_length=255)),
                ('rollback', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('add_sign', models.ManyToManyField(related_name='signer', to=settings.AUTH_USER_MODEL)),
                ('operator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u53d8\u66f4\u7533\u8bf7',
                'verbose_name_plural': '\u53d8\u66f4\u7533\u8bf7',
            },
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('change_time', models.DateTimeField(auto_now=True)),
                ('agree', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=255)),
                ('operator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u52a0\u7b7e',
                'verbose_name_plural': '\u52a0\u7b7e',
            },
        ),
    ]
