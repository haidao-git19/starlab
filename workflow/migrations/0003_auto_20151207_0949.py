# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0002_changeapply_gopass'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sortNo', models.IntegerField()),
                ('actorName', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['sortNo'],
                'verbose_name': '\u6b65\u9aa4',
                'verbose_name_plural': '\u6b65\u9aa4',
            },
        ),
        migrations.CreateModel(
            name='ActorUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actorId', models.ForeignKey(to='workflow.Actor')),
                ('operateUserId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['actorId'],
                'verbose_name': '\u6b65\u9aa4\u5904\u7406\u4eba',
                'verbose_name_plural': '\u6b65\u9aa4\u5904\u7406\u4eba',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemName', models.CharField(max_length=255)),
                ('state', models.IntegerField(default=0, choices=[(0, b'\xe5\xbe\x85\xe5\xae\xa1\xe6\x89\xb9'), (1, b'\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (2, b'\xe6\x8b\x92\xe7\xbb\x9d')])),
                ('itemType', models.IntegerField(null=True, blank=True)),
                ('applyUserId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
        ),
        migrations.CreateModel(
            name='Rout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('routName', models.CharField(max_length=255)),
                ('deptId', models.CharField(max_length=50)),
                ('version', models.IntegerField()),
                ('state', models.IntegerField(choices=[(0, b'\xe8\x8d\x89\xe7\xa8\xbf'), (1, b'\xe5\xb7\xb2\xe5\x8f\x91\xe5\xb8\x83'), (3, b'\xe5\x81\x9c\xe6\xad\xa2')])),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b',
                'verbose_name_plural': '\u6d41\u7a0b',
            },
        ),
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('memo', models.CharField(max_length=255)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('actorId', models.ForeignKey(to='workflow.Actor')),
                ('itemId', models.ForeignKey(to='workflow.Item')),
                ('operateUserId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u5386\u53f2\u8bb0\u5f55',
                'verbose_name_plural': '\u4efb\u52a1\u5386\u53f2\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(choices=[(0, b'\xe6\xa3\x80\xe5\x87\xba'), (1, b'\xe5\xbe\x85\xe6\xa3\x80\xe5\x87\xba')])),
                ('version', models.CharField(max_length=50)),
                ('actorId', models.ForeignKey(to='workflow.Actor')),
                ('itemId', models.ForeignKey(to='workflow.Item')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u5217\u8868',
                'verbose_name_plural': '\u4efb\u52a1\u5217\u8868',
            },
        ),
        migrations.AlterField(
            model_name='changeapply',
            name='add_sign',
            field=models.ManyToManyField(default=[1], related_name='signer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='routID',
            field=models.ForeignKey(to='workflow.Rout'),
        ),
        migrations.AddField(
            model_name='actor',
            name='routId',
            field=models.ForeignKey(to='workflow.Rout'),
        ),
    ]
