from django.db import models
from django.contrib.auth.models import User

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
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
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


