from django.db import models
# from django.conf import settings

from .consts import WAGES, JOB_TYPES
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
    exriry_date = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract = True


class JobsInfo(JobsTimeStamp):
    name = models.CharField(blank=False, null=True, max_length=100)
    user = models.ForeignKey(UserProfile, blank=True, null=True)
    company = models.ForeignKey(CompanyProfile, blank=False, null=True)

    description = models.TextField(
        blank=False, null=True, max_length=100)
    job_type = models.CharField(blank=False,
                                null=True,
                                max_length=100,
                                choices=JOB_TYPES,
                                default='FULL TIME')
    wage = models.CharField(
        blank=False, null=True, max_length=100, choices=WAGES
    )
    experience = models.TextField(blank=False, null=True, max_length=250)
    welfare = models.TextField(blank=False, null=True, max_length=250)
    skill = models.TextField(blank=False, null=True, max_length=250)
    # url when crawler data
    url = models.URLField(blank=True, null=True, max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Detail Jobs Info'
        verbose_name_plural = 'Jobs'
