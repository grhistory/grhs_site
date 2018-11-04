from django.shortcuts import render

def membership(request):
    # render a button for them to pay
    return render(request, 'products/membership.html')

def paypal(request):
    # implement logic for Paypal PDT stuff
    return render(request, 'products/paypal.html')
