from django.contrib import admin

from .models import Newsletters


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'full_name', 'created', 'updated']


admin.site.register(Newsletters, NewsletterAdmin)
