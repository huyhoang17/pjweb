from django.contrib import admin

from .models import CompanyProfile, Membership
from job.models import JobsInfo
# Register your models here.


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    max_num = 10


class JobsInfoInline(admin.StackedInline):
    model = JobsInfo
    extra = 0
    max_num = 10


class MembershipAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id']


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'city',
        'created',
        'updated',
    ]
    list_filter = (
        "created",
        "updated"
    )
    inlines = [MembershipInline, JobsInfoInline, ]
    search_fields = [
        'name',
        'address',
        'city',
        'website'
    ]
    readonly_fields = ["created", "updated"]

    class Meta:
        model = CompanyProfile


admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(Membership, MembershipAdmin)
