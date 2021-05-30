from django.contrib import admin
from scheduler.models import *

# Register your models here.
# admin.site.register(Slot)
admin.site.register(Customer)


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    fields = (
        "timezone",
        ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"),
        "start_date",
        ("start_time", "end_time"),
        ("interval", "early_notice"),
    )
