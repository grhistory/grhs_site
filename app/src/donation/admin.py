from django.contrib import admin
from .models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'donation_amount']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['donation_amount']


admin.site.register(Donation, DonationAdmin)
