from django import forms
from nok_web.checklist.app_models.organisations import Organisations


class OrganisationsForm(forms.ModelForm):
    class Meta:
        model = Organisations
        fields = ['organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota', 'is_deleted']
        widgets = {
            'organisation_name': forms.TextInput(attrs={"class": "form-control"}),
            'address': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'website': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
            'parent': forms.Select(attrs={"class": "form-control"}),
            'department': forms.Select(attrs={"class": "form-control"}),
            'quota': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }