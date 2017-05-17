from django import forms

from .models import Newsletters


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True)


class NewslettersForm(forms.ModelForm):
    class Meta:
        model = Newsletters
        fields = ['full_name', 'email']
