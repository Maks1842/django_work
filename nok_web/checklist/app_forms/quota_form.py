from django import forms
from nok_web.checklist.app_models.quota import Quota


class QuotaForm(forms.ModelForm):
    class Meta:
        model = Quota
        fields = ['quota']
        widgets = {
            'quota': forms.TextInput(attrs={"class": "form-control"}),
        }