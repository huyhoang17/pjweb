from django import forms

from .models import JobsInfo


class JobCreateForm(forms.ModelForm):

    class Meta:
        model = JobsInfo
        fields = [
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
