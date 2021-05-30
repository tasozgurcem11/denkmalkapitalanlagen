from django.contrib import admin
from .models import Email, Kontakt
import csv
from django.http import HttpResponse, HttpResponseRedirect, request  # noqa: 401


# Register your models here.
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export als CSV(Excel-Format)"


# class UserInfo(admin.ModelAdmin):
#
#     list_display = ("email", "created_at")

class KontaktInfo(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    list_display = ("vorname", "nachname", "email", "quelle", "created_at")


# admin.site.register(Email, UserInfo)
admin.site.register(Kontakt, KontaktInfo)

