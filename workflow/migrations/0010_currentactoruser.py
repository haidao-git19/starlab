# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0009_auto_20151215_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentActorUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'\xe5\x9b\xba\xe5\xae\x9a\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba'), (1, b'\xe5\x8a\xa0\xe7\xad\xbe\xe5\xae\xa1\xe6\x89\xb9\xe4\xba\xba')])),
                ('state', models.NullBooleanField(default=None)),
                ('actorUser', models.ForeignKey(to='workflow.ActorUser')),
                ('operateUserId', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='workflow.TaskList')),
            ],
        ),
    ]
