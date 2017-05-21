from django.contrib import admin

from .models import JobsInfo
# Register your models here.


class JobsInfoAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "updated",
    ]
    list_display_links = ["updated"]
    list_editable = ["name"]
    list_filter = (
        "created",
        "updated"
    )
    list_per_page = 25
    readonly_fields = ["created", "updated"]
    search_fields = [
        "name",
        "company",
        "description",
        "job_type",
        "skill",
    ]

    class Meta:
        model = JobsInfo


admin.site.register(JobsInfo, JobsInfoAdmin)
