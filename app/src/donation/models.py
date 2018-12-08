from django.db import models
from django.shortcuts import render, redirect
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

# Create your models here.
class Donation(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(blank=True,null=True)
    donation_amount = models.DecimalField(max_digits=6, decimal_places=2)
    address1 = models.CharField(max_length=124)
    address2 = models.CharField(max_length=124, blank=True, null=True)
    zip_code = models.CharField(max_length=12)
    city = models.CharField(max_length=124)
    state = models.CharField(max_length=25)
    telephone = models.CharField(max_length=25, blank=True, null=True)
    create_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    paid_on = models.DateField(blank=True, null=True)

class DonationPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="This will override the title of the page.")
    intro = RichTextField(blank=True)

    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="subtitle"),
        FieldPanel('intro', classname="full"),
    ]

    def serve(self, request):
        from donation.forms import DonationForm

        if request.method == 'POST':
            form = DonationForm(request.POST)
            if form.is_valid():
                donation = form.save()
                request.session['payment'] = {'type': 'donation', 'id': donation.id}
                return redirect('/payment/donation/{}'.format(donation.id))
        else:
            form = DonationForm()

        return render(request, 'donation/donation_form.html', {
            'page': self,
            'form': form,
        })

