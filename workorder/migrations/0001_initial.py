# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('sort', models.IntegerField()),
            ],
            options={
                'verbose_name': '\u5206\u6b65\u9aa4',
                'verbose_name_plural': '\u5206\u6b65\u9aa4',
            },
        ),
        migrations.CreateModel(
            name='ActorUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'\xe5\x9b\xba\xe5\xae\x9a\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba'), (1, b'\xe5\x8a\xa0\xe7\xad\xbe\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba')])),
                ('actor', models.ForeignKey(related_name='actoruseractor', to='workorder.Actor')),
                ('name', models.ForeignKey(related_name='actorusername', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6b65\u9aa4\u5904\u7406\u4eba',
                'verbose_name_plural': '\u6b65\u9aa4\u5904\u7406\u4eba',
            },
        ),
        migrations.CreateModel(
            name='Category1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('defaultOperator', models.ForeignKey(related_name='categorydefaultuser', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(related_name='category1group', to='auth.Group')),
                ('manager', models.ForeignKey(related_name='category1manager', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5927\u7c7b',
                'verbose_name_plural': '\u5927\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Category2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('category1', models.ForeignKey(to='workorder.Category1')),
            ],
            options={
                'verbose_name': '\u5c0f\u7c7b',
                'verbose_name_plural': '\u5c0f\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='CurrentActorUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'\xe5\x9b\xba\xe5\xae\x9a\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba'), (1, b'\xe5\x8a\xa0\xe7\xad\xbe\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba')])),
                ('actor', models.ForeignKey(related_name='currentactoruseractor', to='workorder.Actor')),
                ('name', models.ForeignKey(related_name='currentactorusername', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5f53\u524d\u6b65\u9aa4\u5904\u7406\u4eba',
                'verbose_name_plural': '\u5f53\u524d\u6b65\u9aa4\u5904\u7406\u4eba',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('startdatetime', models.DateTimeField(auto_now_add=True)),
                ('state', models.IntegerField(default=0, verbose_name=b'\xe5\xb7\xa5\xe5\x8d\x95\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xbe\x85\xe5\x88\x9b\xe5\xbb\xba\xe4\xbb\xbb\xe5\x8a\xa1'), (1, b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe5\xb7\xa5\xe5\x8d\x95\xe5\xb7\xb2\xe5\x85\xb3\xe9\x97\xad')])),
                ('enddatetime', models.DateTimeField(null=True, blank=True)),
                ('purpose', models.CharField(max_length=5000, null=True, verbose_name=b'\xe7\x9b\xae\xe7\x9a\x84', blank=True)),
                ('comment', models.CharField(max_length=5000, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('category1', models.ForeignKey(related_name='ordercategory1', to='workorder.Category1')),
                ('category2', models.ForeignKey(related_name='ordercategory2', to='workorder.Category2')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5de5\u5355',
                'verbose_name_plural': '\u5de5\u5355',
            },
        ),
        migrations.CreateModel(
            name='Rout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u6a21\u677f',
                'verbose_name_plural': '\u6d41\u7a0b\u6a21\u677f',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('actor', models.ForeignKey(related_name='taskactor', to='workorder.Actor')),
                ('operator', models.ForeignKey(related_name='taskoperator', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('order', models.ForeignKey(related_name='taskorder', to='workorder.Order')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1',
                'verbose_name_plural': '\u4efb\u52a1',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='rout',
            field=models.ForeignKey(related_name='orderrout', to='workorder.Rout'),
        ),
        migrations.AddField(
            model_name='currentactoruser',
            name='task',
            field=models.ForeignKey(related_name='task', to='workorder.Task'),
        ),
        migrations.AddField(
            model_name='actor',
            name='rout',
            field=models.ForeignKey(to='workorder.Rout'),
        ),
    ]
