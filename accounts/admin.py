from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
    list_display = ['__str__', 'created', 'updated',
                    'id', 'bio', 'location', 'birth_date']
    inlines = [MembershipInline, JobsInfoInline, ]
    search_fields = ['__str__', 'bio', 'location', 'skill', 'phone_number']
    # list_filter = ('skill',)
    # date_hierarchy = (,)
    # show_full_result_count = True


# admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
