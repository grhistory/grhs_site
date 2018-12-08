import urllib.parse
import requests
import datetime
from django.shortcuts import render, redirect
from membership.models import Membership
from donation.models import Donation
from products.models import PaypalSettings

def donation(request, id):
    try:
        donation = Donation.objects.get(id=id)
        return render(request, 'products/payment.html', {'item_name': 'Donation', 'amount': donation.donation_amount});
    except Donation.DoesNotExist:
        return render(request, 'products/error.html')

def membership(request, id):
    try:
        member = Membership.objects.get(id=id)
        if member.member_type == 'I':
            member_type = 'Individual'
            amount = 30
        elif member.member_type == 'St':
            member_type = 'Student'
            amount = 20
        elif member.member_type == 'L':
            member_type = 'Legacy'
            amount = 400
        elif member.member_type == 'SE':
            member_type = 'Senior'
            amount = 20
        # double check they have not already been through here
        member.amount = amount
        member.save(update_fields=['amount'])
        return render(request, 'products/payment.html', {'item_name': member_type + ' Membership', 'amount': amount})
    except Membership.DoesNotExist:
        return render(request, 'products/error.html')

def paypal(request):
    # implement logic for Paypal PDT stuff
    payment = request.session.get('payment', None)
    if payment is None:
        return render(request, 'products/paypal.html')

    if request.GET.get('tx'):
        if validate(request, PaypalSettings.for_site(request.site)):
            if payment['type'] == 'membership':
                member = Membership.objects.get(id=payment['id'])
                member.dues_paid = datetime.date.today()
                member.start_date = datetime.datetime.today()
                member.save(update_fields=['dues_paid', 'start_date'])
            elif payment['type'] == 'donation':
                donation = Donation.objects.get(id=payment['id'])
                donation.paid_on = datetime.date.today()
                donation.save(update_fields=['paid_on'])
            request.session['payment'] = None
            return render(request, 'products/paypal.html')
        else:
            return render(request, 'products/error.html')
    else:
        return render(request, 'products/error.html')


def validate(request, settings):
    tx = request.GET.get('tx')
    headers = {'content-type': 'application/x-www-form-urlencoded',
                       'user-agent': 'Python-PDT-Verification-Script'}
    params = {'tx': tx,
            'cmd': '_notify-synch',
            'at': settings.identity_token}
    url = 'https://{}/cgi-bin/webscr'.format(settings.url)
    r = requests.post(url, params=params, headers=headers, verify=True)
    r.raise_for_status()
    data = r.text.split('\n')
    # mc_gross = next(x for x in data if 'mc_gross' in x) # mc_gross = 'mc_gross=xx.xx'
    status = data.pop(0)
    return status == 'SUCCESS'


