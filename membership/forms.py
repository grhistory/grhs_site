from django import forms
from django.forms import forms, ModelForm
from .models import Membership

class MembershipForm(ModelForm):

    class Meta:
        model = Membership
        fields = [
            'first_name',
            'last_name',
            'address1',
            'address2',
            'city',
            'state',
            'country',
            'zip_code',
            'email',
            'telephone',
            'member_type',

        ]