from django.contrib import admin
from .models import *
# Register your models here.



class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'category2', 'state', 'owner')

admin.site.register(Rout)
admin.site.register(Actor)
admin.site.register(ActorUser)
admin.site.register(CurrentActorUser)
admin.site.register(Order, OrderAdmin)
admin.site.register(Task)
admin.site.register(Category1)
admin.site.register(Category2)
admin.site.register(ProposerManager)

