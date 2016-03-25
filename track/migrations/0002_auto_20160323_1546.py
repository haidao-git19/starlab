# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='comment',
            field=models.CharField(default=None, max_length=5000),
        ),
        migrations.AddField(
            model_name='event',
            name='current_people',
            field=models.ForeignKey(related_name='current_people', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(related_name='category', to='track.EventCategory'),
        ),
        migrations.AlterField(
            model_name='event',
            name='level',
            field=models.ForeignKey(related_name='level', to='track.Level'),
        ),
        migrations.AlterField(
            model_name='event',
            name='offer_people',
            field=models.ForeignKey(related_name='offer_people', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.ForeignKey(related_name='event_status', to='track.EventStatus'),
        ),
    ]
