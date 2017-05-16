from django.contrib import admin

from .models import UserProfile
from companys.models import Membership
from job.models import JobsInfo
# Register your models here.


# class UserProfileInline(admin.TabularInline):
#     model = User
#     extra = 0
#     max_num = 10


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'id', 'bio', 'location', 'birth_date']
#     inlines = [
#         UserProfileInline,
#     ]

#     class Meta:
#         model = UserProfile


# admin.site.register(UserProfile, UserProfileAdmin)


# admin.site.unregister(User)


# class UserProfileInline(admin.StackedInline):
#     model = UserProfile


# class UserProfileAdmin(UserAdmin):
#     inlines = [UserProfileInline, ]


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
        # 'location'
        'created',
        'updated',
    ]
    list_display_links = ["updated"]
    list_filter = (
        "created",
        "updated"
    )
    # inlines = [MembershipInline, JobsInfoInline, ]
    search_fields = ['__str__', 'bio', 'location', 'skill', 'phone_number']
    readonly_fields = ["created", "updated"]


# admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
