import csv
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Membership
import csv
from django.http import HttpResponse

class EmailFilter(admin.SimpleListFilter):
    title = 'has email'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'email__isnull'

    def lookups(self, request, model_admin):
        return (
            ('False', 'has email'),
            ('True', 'has no email'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'False':
            return queryset.filter(email__isnull=False)
        if self.value() == 'True':
            return queryset.filter(email__isnull=True)

class MembershipAdmin(admin.ModelAdmin):

    list_display = ["user", "agency", "first_name", "last_name", "email", "get_member_type", "start_date", "end_date", "is_active"]
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['member_type', 'billing_quarter', 'start_date', 'end_date', 'is_active', EmailFilter]
    list_editable = ('is_active', )
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
