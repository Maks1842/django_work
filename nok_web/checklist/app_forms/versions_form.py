from django import forms
from nok_web.checklist.app_models.versions import Versions


class VersionsForm(forms.ModelForm):
    class Meta:
        model = Versions
        fields = ['table_name', 'version', 'active', 'is_deleted']
        widgets = {
            'table_name': forms.TextInput(attrs={"class": "form-control"}),
            'version': forms.TextInput(attrs={"class": "form-control"}),
            'active': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }