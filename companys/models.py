from django.db import models
from django.utils.text import slugify

import datetime

from .consts import SIZE_COMPANY, CITY
from accounts.models import UserProfile
# Create your models here.


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class Membership(models.Model):
    account = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + '-' + self.company.name


def image_upload_to(instance, filename):
    '''
    PARAMS: 2 default params
        instance: this models
        filename:
    '''
    title = instance.name  # company name
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "{}-{}.{}".format(slug, instance.id, file_extension)
    return "company/{}/{}".format(slug, new_filename)


class CompanyProfile(TimeStamp):
    member = models.ManyToManyField(UserProfile, through='Membership')
    name = models.CharField(blank=True, null=True, max_length=50)
    description = models.TextField(blank=True, null=True, max_length=500)
    address = models.CharField(blank=True, null=True, max_length=50)
    city = models.CharField(
        blank=True, null=True, max_length=50, choices=CITY
    )
    country = models.CharField(
        blank=True, null=True, max_length=50, default='Viet Nam'
    )
    phone_number = models.CharField(blank=True, null=True, max_length=250)
    website = models.CharField(blank=True, null=True, max_length=250)
    logo = models.ImageField(upload_to=image_upload_to,
                             null=True,
                             blank=True,
                             help_text="Upload logo for Company")
    size = models.CharField(max_length=120, choices=SIZE_COMPANY)

    email_contact = models.EmailField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Detail Company Info'
        verbose_name_plural = 'Companys'
