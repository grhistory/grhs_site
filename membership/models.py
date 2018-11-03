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
    REGULAR = "R"
    STUDENT = "S"
    LIFETIME = "L"
    COMPLIMENTARY = "C"
    MEMBER_TYPES = (
        (REGULAR, 'Regular'),
        (STUDENT, 'Student'),
        (LIFETIME, 'Lifetime'),
        (COMPLIMENTARY, "Complimentary")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    initial = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(blank=True,null=True)
    title = models.CharField(max_length=25, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    member_type = models.CharField(max_length=25, choices=MEMBER_TYPES, default=REGULAR)
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
    newsletter = models.BooleanField(default=False)
    create_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


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

class MembershipRegistrationPage(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page")
    thank_you_text = RichTextField(blank=True, help_text="Text for the user to see on registration confirmation")

    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    content_panels = Page.content_panels + [
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
                return redirect('/payment/membership/{}'.format(registration.id))
        else:
            form = MembershipForm()

        return render(request, 'membership/membership_registration.html', {
            'page': self,
            'form': form,
        })
