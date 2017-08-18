from django import forms
from business.models import Authapply
from .validators import PhonenumberValidator


class BusinessApplyForm(forms.ModelForm):
    phonenumber = forms.CharField(max_length=11, required=True, validators=[PhonenumberValidator()])

    class Meta:
        model = Authapply
        fields = [
            'name',
            'position',
            'floor',
            'type'
        ]
