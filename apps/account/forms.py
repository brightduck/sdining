from django import forms
from django.core.exceptions import ValidationError

from business.models import Authapply


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=150)
    password = forms.CharField(required=True)


class BusinessApplyForm(forms.ModelForm):
    class Meta:
        model = Authapply
        fields = [
            'name',
            'position',
            'floor',
            'type'
        ]
