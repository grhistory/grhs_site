import urllib.parse
import requests
import datetime
from django.shortcuts import render, redirect
from membership.models import Membership
from products.models import PaypalSettings

def membership(request, id):
    # render a button for them to pay
    try:
        member = Membership.objects.get(id=id)
        if member.member_type == 'I':
            member_type = 'Individual'
        elif member.member_type == 'St':
            member_type = 'Student'
        elif member.member_type == 'L':
            member_type = 'Legacy'
        elif member.member_type == 'SE':
            member_type = 'Senior'
        # double check they have not already been through here
        return render(request, 'products/membership.html', {'member': member, 'member_type': member_type})
    except Membership.DoesNotExist:
        return render(request, 'products/error.html')

def paypal(request):
    # implement logic for Paypal PDT stuff
    registration_id = request.session.get('registration_id', None)
    if registration_id is None:
        return redirect('/')

    if request.GET.get('tx'):
        tx = request.GET.get('tx')
        settings = PaypalSettings.for_site(request.site)
        headers = {'content-type': 'application/x-www-form-urlencoded',
                           'user-agent': 'Python-PDT-Verification-Script'}
        params = {'tx': tx,
                'cmd': '_notify-synch',
                'at': settings.identity_token}
        url = 'https://{}/cgi-bin/webscr'.format(settings.url)
        r = requests.post(url, params=params, headers=headers, verify=True)
        r.raise_for_status()
        data = r.text.split('\n')
        status = data.pop(0)
        if status== 'SUCCESS':
            mc_gross = next(x for x in data if 'mc_gross' in x) # mc_gross = 'mc_gross=xx.xx'
            member = Membership.objects.get(id=registration_id)
            member.dues_paid = datetime.date.today()
            member.start_date = datetime.datetime.today()
            member.save(update_fields=['dues_paid', 'start_date'])
            request.session['registration_id'] = None
            return render(request, 'products/paypal.html')
        else:
            return render(request, 'products/error.html')
    else:
        return render(request, 'products/error.html')




