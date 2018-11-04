from django import forms
from django.forms import  ModelForm
from .models import Donation

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = [
            'first_name',
            'last_name',
            'address1',
            'address2',
            'city',
            'state',
            'zip_code',
            'email',
            'telephone',
            'donation_amount',
        ]
