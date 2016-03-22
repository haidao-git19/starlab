# coding:utf8
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class Level(models.Model):
    name = models.CharField(max_length=255)
    time_since = models.IntegerField(help_text=u'默认8小时', default=8, null=True, blank=True)

    def __unicode__(self):
        return str(self.name)


class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey("auth.User")

    def __unicode__(self):
        return str(self.name)


class EventStatus(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.name)

class Event(models.Model):
    name = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    desc = models.CharField(max_length=5000)
    level = models.ForeignKey("track.Level", verbose_name="level")
    offer_people = models.ForeignKey("auth.User", verbose_name="offer_people")
    category = models.ForeignKey("track.EventCategory", verbose_name="category")
    status = models.ForeignKey("track.EventStatus", verbose_name="event_status")

    def __unicode__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('track:event-detail', kwargs={'pk': self.id})