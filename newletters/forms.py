from django import forms

from .models import Newsletters


class ContactForm(forms.Form):
    full_name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField()


class NewslettersForm(forms.ModelForm):
    class Meta:
        model = Newsletters
        fields = ['full_name', 'email']
