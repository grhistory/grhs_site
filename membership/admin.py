from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Membership


class MembershipAdmin(admin.ModelAdmin):

    list_display = ["user", "first_name", "last_name", "email", "member_type", "start_date", "end_date"]


admin.site.register(Membership, MembershipAdmin)