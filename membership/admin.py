import csv
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Membership
import csv
from django.http import HttpResponse

class MembershipAdmin(admin.ModelAdmin):

    list_display = ["user", "first_name", "last_name", "email", "get_member_type", "start_date", "end_date"]
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['member_type', 'start_date', 'end_date']
    actions = ['export_to_csv']
    def get_member_type(self, obj):
        return obj.get_member_type_display()
    get_member_type.short_description = 'Member Type'
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response


    export_to_csv.short_description = "Export to CSV"


admin.site.register(Membership, MembershipAdmin)