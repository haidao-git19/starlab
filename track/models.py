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
    desc = models.TextField(max_length=5000, null=True, blank=True, verbose_name=u"跟踪日志")
    level = models.ForeignKey("track.Level", related_name="level")
    offer_people = models.ForeignKey("auth.User", related_name="offer_people")
    category = models.ForeignKey("track.EventCategory", related_name="category")
    current_people = models.ForeignKey("auth.User", related_name="current_people", verbose_name=u"当前责任人")
    status = models.ForeignKey("track.EventStatus", related_name="event_status")
    comment = models.CharField(max_length=5000, null=True, blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('track:event-detail', kwargs={'pk': self.id})