# coding:utf8
from django.db import models
from django.contrib import admin

# Create your models here.


class Website(models.Model):
    name = models.CharField(max_length=20)
    url = models.URLField()
    order = models.IntegerField(default=0, verbose_name=u"排序")
    img = models.ImageField(upload_to='img', verbose_name=u"配图(注意比例)")
    description = models.CharField(max_length=100, verbose_name=u"描述")
    owner = models.ForeignKey("auth.User", verbose_name=u"管理员")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = "观星台"
        verbose_name_plural = "观星台"
# admin.site.register(Snippet)


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'description', 'owner')
admin.site.register(Website, WebsiteAdmin)