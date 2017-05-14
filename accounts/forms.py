from django import forms

from .models import UserProfile


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "location",
            "birth_date",
            "skill",
            "phone_number",
            "avatar",
            "cv_user",
        ]
