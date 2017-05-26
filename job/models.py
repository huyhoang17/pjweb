from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from .consts import JOB_TYPES
from accounts.models import UserProfile
from companys.models import CompanyProfile


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
    name = models.CharField(blank=False, null=True, max_length=255)
    slug = models.SlugField(blank=True, max_length=255)
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
                            max_length=255,
                            default="Unknown")
    experience = models.TextField(blank=False, null=True, max_length=1000)
    welfare = models.TextField(blank=False, null=True, max_length=1000)
    skill = models.TextField(blank=False, null=True, max_length=1000)
    # url when crawler data
    url = models.URLField(blank=True, null=True, max_length=255)
    exriry_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def get_raw_string(self):
        s = self.description
        return "\n".join(s.split("|"))

    @property
    def get_username(self):
        return self.user.user.username

    def get_job_apply_url(self):
        '''
        https://itviec.com/ --> itviec.com
        '''
        return self.url.split('//')[1].split('/')[0]

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
