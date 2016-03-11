from django.contrib import admin
from .models import Receiver

# Register your models here.
class ReceiverAdmin(admin.ModelAdmin):
    using = 'stationdb'
    list_display = ('id', 'rec_sn', 'category_id', 'rec_type', 'station_ip', 'station_pm', 'station_agent_owner', 'station_agent_contact')
    search_fields = ('rec_sn',)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(ReceiverAdmin, self).get_queryset(request).using(self.using)



admin.site.register(Receiver, ReceiverAdmin)