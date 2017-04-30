from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save

import datetime
# Create your models here.


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


def image_upload_to(instance, filename):
    '''
    PARAMS: 2 default params
        instance: this models
        filename:
    '''
    name = instance.user.username  # company name
    user_id = instance.user.id
    user = name + str(user_id)
    basename, file_extension = filename.split(".")
    new_filename = "{}-{}.{}".format(user, instance.id, file_extension)
    return "user/{}/{}".format(user, new_filename)


class UserProfile(TimeStamp):
    user = models.OneToOneField(
        User, related_name='accounts', on_delete=models.CASCADE)
    # company = models.ForeignKey(CompanyProfile, blank=True, null=True)

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="""
            Phone number must be entered in the format: '+999999999'. \
            Up to 15 digits allowed.
        """
    )
    skill = models.TextField(blank=True, null=True, max_length=250)
    phone_number = models.CharField(max_length=20,
                                    validators=[phone_regex],
                                    blank=True,
                                    null=True)
    avatar = models.ImageField(upload_to=image_upload_to,
                               null=True,
                               blank=True,
                               help_text="Upload Your Avatar")
    cv_user = models.FileField(upload_to=image_upload_to,
                               null=True,
                               blank=True,
                               help_text="Upload Your CV")

    # job_saved = models.

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Detail User Profile'
        verbose_name_plural = 'Users'


# def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
#     pass


# post_save.connect(cart_item_post_save_receiver, sender=UserProfile)
