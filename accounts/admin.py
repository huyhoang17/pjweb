from django.contrib import admin

from .models import UserProfile
from companys.models import Membership
from job.models import JobsInfo


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    max_num = 10


class JobsInfoInline(admin.StackedInline):
    model = JobsInfo
    extra = 0
    max_num = 10


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'pk',
        'created',
        'updated',
    ]
    list_display_links = ["updated"]
    list_filter = (
        "created",
        "updated"
    )
    search_fields = ['bio', 'location', 'skill', 'phone_number']
    readonly_fields = ["created", "updated"]


admin.site.register(UserProfile, UserProfileAdmin)
