from django import forms

from .models import CompanyProfile


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "name",
            "description",
            "address",
            "city",
            "country",
            "phone_number",
            "website",
            "logo",
            "size",
            "email_contact",
        ]
