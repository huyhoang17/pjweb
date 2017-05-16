from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
# from django.conf import settings

from .consts import JOB_TYPES
from companys.models import CompanyProfile
from accounts.models import UserProfile
# Create your models here.


class JobsDetailRank(models.Model):
    # upvoted
    # job_saved
    pass


class JobsTimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class JobsInfo(JobsTimeStamp):
    name = models.CharField(blank=False, null=True, max_length=100)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    company = models.ForeignKey(CompanyProfile, blank=False, null=True)

    description = models.TextField(blank=False,
                                   null=True,
                                   max_length=1000)

    job_type = models.CharField(blank=False,
                                null=True,
                                max_length=100,
                                choices=JOB_TYPES,
                                default='FULL TIME')

    wage = models.CharField(blank=False,
                            null=True,
                            max_length=100,
                            default="Unknown")
    experience = models.TextField(blank=False, null=True, max_length=1000)
    welfare = models.TextField(blank=False, null=True, max_length=1000)
    skill = models.TextField(blank=False, null=True, max_length=250)
    # url when crawler data
    url = models.URLField(blank=True, null=True, max_length=250)
    exriry_date = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    @property
    def get_raw_string(self):
        s = self.description.split('|')
        return "\n".join(s)

    def get_absolute_url(self):
        return reverse(
            "detail_jobs",
            kwargs={"pk": self.pk, "slug": self.slug}
        )

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ["-id"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = JobsInfo.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_job_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_job_receiver, sender=JobsInfo)
