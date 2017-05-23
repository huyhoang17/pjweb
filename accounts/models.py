from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from registration.models import RegistrationProfile


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


def image_upload_to(instance, filename):
    '''
    :param instance: this models
    :param filename:
    '''
    name = instance.user.username  # company name
    user_id = instance.user.id
    user = name + str(user_id)
    basename, file_extension = filename.split(".")
    new_filename = "{}-{}.{}".format(user, instance.id, file_extension)
    return "user/{}/{}".format(user, new_filename)


class UserProfile(TimeStamp):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    # company = models.ForeignKey(CompanyProfile, blank=True, null=True)
    slug = models.SlugField(blank=True, max_length=255, default='user-profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
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

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("detail_accounts",
                       kwargs={"pk": self.pk, "slug": self.slug})

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-updated", "-id"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.username)
    if new_slug is not None:
        slug = new_slug
    qs = UserProfile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_job_receiver(sender, instance, *args, **kwargs):
    if not instance.slug or instance.slug == "user-profile":
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_job_receiver, sender=UserProfile)


def pre_save_job_receiver(sender, instance, *args, **kwargs):
    if instance.activated:
        user_acc = UserProfile(user=instance.user)
        user_acc.save()


pre_save.connect(pre_save_job_receiver, sender=RegistrationProfile)


def register_user_admin_profile_pre_save(sender, instance, **kwargs):
    '''
    :param sender: base.ModelBase obj
    :param instance: User ojb
    '''
    try:
        UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        # UserProfile(user=instance)
        UserProfile.objects.create(user=instance)


post_save.connect(register_user_admin_profile_pre_save, sender=User)
