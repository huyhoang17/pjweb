from django import forms
# from django.contrib.admin import widgets

from .models import JobsInfo


class JobCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['exriry_date'].widget = widgets.AdminSplitDateTime()

    class Meta:
        model = JobsInfo
        fields = [
            # "company_name",
            "name",
            "description",
            "job_type",
            "wage",
            "experience",
            "welfare",
            "skill",
            "url",
            "exriry_date"
        ]
