from django.contrib import admin

from .models import JobsInfo
# Register your models here.


class JobsInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'name', 'wage']


admin.site.register(JobsInfo, JobsInfoAdmin)
