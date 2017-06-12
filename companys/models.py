from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from .consts import CITY, SIZE_COMPANY
from accounts.models import UserProfile


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class Membership(models.Model):
    account = models.ForeignKey(UserProfile)
    company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.account.user.username + '-' + self.company.name


def image_upload_to(instance, filename):
    title = instance.name  # company name
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "{}-{}.{}".format(slug, instance.id, file_extension)
    return "company/{}/{}".format(slug, new_filename)


class CompanyProfile(TimeStamp):
    member = models.ManyToManyField(UserProfile,
                                    through='Membership',
                                    blank=True)
    name = models.CharField(blank=True,
                            max_length=255,
                            default='company-profile')
    slug = models.SlugField(blank=True, max_length=255)
    description = models.TextField(blank=True, null=True, max_length=1000)
    address = models.CharField(blank=True, null=True, max_length=255)

    city = models.CharField(blank=True,
                            null=True,
                            max_length=255,
                            choices=CITY,
                            default="Ha Noi")
    country = models.CharField(blank=True,
                               null=True,
                               max_length=255,
                               default='Viet Nam')

    phone_number = models.CharField(blank=True, null=True, max_length=250)
    website = models.CharField(blank=True, null=True, max_length=250)

    logo = models.ImageField(upload_to=image_upload_to,
                             null=True,
                             blank=True,
                             help_text="Upload logo for Company")

    size = models.CharField(max_length=255,
                            null=True,
                            blank=False,
                            choices=SIZE_COMPANY)

    email_contact = models.EmailField(max_length=255,
                                      null=True,
                                      blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail_companys",
                       kwargs={"pk": self.pk, "slug": self.slug})

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companys"
        ordering = ["-id"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = CompanyProfile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_company_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_company_receiver, sender=CompanyProfile)
