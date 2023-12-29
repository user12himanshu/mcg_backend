from django.contrib import admin
from .models import *


# Register your models here.
class SlotAdmin(admin.ModelAdmin):
    list_display = ["date", "start_time", "end_time","booked", 'type']
    # readonly_fields = ["tickets_left"]


admin.site.register(Slot, SlotAdmin)
admin.site.register(Charges)
