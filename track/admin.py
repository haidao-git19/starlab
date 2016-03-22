from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(Level)
admin.site.register(EventStatus)