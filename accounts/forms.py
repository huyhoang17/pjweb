from django import forms

from .models import UserProfile


class AccountCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = kwargs.get("instance").user.email

    class Meta:
        model = UserProfile
        fields = [
            "email",
            "bio",
            "location",
            "birth_date",
            "skill",
            "phone_number",
            "avatar",
            "cv_user",
        ]
