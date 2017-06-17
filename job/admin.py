from django.contrib import admin

from .models import JobsInfo


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
    make_active.short_description = "Mark selected jobs as actived"


class JobsInfoAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "pk",
        "active",
        "user",
        "company",
        "created",
        "updated",
    ]
    list_display_links = ["created", "updated"]
    list_editable = ["active", "name"]
    list_filter = (
        "user",
        "active",
        "created",
        "updated"
    )
    list_per_page = 50
    readonly_fields = ["created", "updated"]
    search_fields = [
        "name",
        "description",
        "job_type",
        "skill",
    ]
    actions = [make_active]

    class Meta:
        model = JobsInfo


admin.site.register(JobsInfo, JobsInfoAdmin)
