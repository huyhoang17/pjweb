from django import forms

from .models import JobsInfo


class JobCreateForm(forms.ModelForm):
    company_name = forms.CharField(disabled=True)

    def __init__(self, *args, **kwargs):
        '''
        :param kwargs["instance"]: company name
        '''
        super().__init__(*args, **kwargs)
        self.fields["company_name"].initial = kwargs.get("instance", None)
        # self.fields['company'].widget.attrs['readonly'] = True

    class Meta:
        model = JobsInfo
        fields = [
            "company_name",
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
