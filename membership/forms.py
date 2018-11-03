from django import forms
from django.forms import  ModelForm
from .models import Membership

class MembershipForm(ModelForm):
    MEMBER_STATUS = (
        ("new", "New"),
        ("renew", "Renew"),
    )
    membership_status = forms.ChoiceField(choices=MEMBER_STATUS)
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
            'membership_status'

        ]
