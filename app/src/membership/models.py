from django.db import models
from django.contrib.auth.models import User


from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page

from django.db import models
from django.shortcuts import render, redirect


from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

# Create your models here.
class Membership(models.Model):
    INDIVIDUAL = "I"
    STUDENT = "St"
    LEGACY = "L"
    COMPLIMENTARY = "C"
    SENIOR = "SE"
    BAXTER = "B"
    MEMBER_TYPES = (
        (INDIVIDUAL, 'Individual'),
        (SENIOR, 'Senior'),
        (STUDENT, "Student"),
        (LEGACY, 'Legacy'),
        (COMPLIMENTARY, "Complimentary"),
        (BAXTER, "Baxter"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    initial = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(blank=True,null=True)
    title = models.CharField(max_length=25, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    member_type = models.CharField(max_length=25, choices=MEMBER_TYPES, default=INDIVIDUAL)
    agency = models.CharField(max_length=124, blank=True, null=True)
    address1 = models.CharField(max_length=124)
    address2 = models.CharField(max_length=124, blank=True, null=True)
    zip_code = models.CharField(max_length=12)
    city = models.CharField(max_length=124)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    telephone = models.CharField(max_length=25, blank=True, null=True)
    work_telephone = models.CharField(max_length=25, blank=True, null=True)
    newsletter_email = models.EmailField(blank=True, null=True)
    billing_quarter = models.CharField(max_length=25, blank=True, null=True)
    dues_paid = models.DateField(blank=True, null=True)
    print_newsletter = models.BooleanField(default=False)
    digital_newsletter = models.BooleanField(default=False)
    create_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)


    def save(self, *args, **kwargs):
        if not self.user:
            if self.email:
                obj, created = User.objects.get_or_create(
                    email=self.email,
                )
                if created:
                    obj.first_name = self.first_name
                    obj.last_name = self.last_name
                    obj.username = "{} {}".format(self.first_name, self.last_name)
                    obj.save()
                self.user = obj

        super(Membership, self).save(*args, **kwargs)

class MembershipApplication(Page):
    subtitle = models.CharField(max_length=255, blank=True, help_text="This will override the title of the page.")
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page")
    thank_you_text = RichTextField(blank=True, help_text="Text for the user to see on registration confirmation")

    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="subtitle"),
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
        FieldPanel('thank_you_text'),
    ]
    def serve(self, request):
        from membership.forms import MembershipForm

        if request.method == 'POST':
            form = MembershipForm(request.POST)
            if form.is_valid():
                registration = form.save()
                request.session['payment'] = {'type': 'membership', 'id': registration.id}
                return redirect('/payment/membership/{}'.format(registration.id))
        else:
            form = MembershipForm()

        return render(request, 'membership/membership_application.html', {
            'page': self,
            'form': form,
        })
