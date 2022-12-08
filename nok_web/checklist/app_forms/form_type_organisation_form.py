from django import forms
from ..app_models.form_type_organisation import Form_Type_Organisation


class Form_Type_OrganisationForm(forms.ModelForm):
    class Meta:
        model = Form_Type_Organisation
        fields = ['organisation', 'type_organisation']
        widgets = {
            'organisation': forms.Select(attrs={"class": "form-control"}),
            'type_organisation': forms.Select(attrs={"class": "form-control"})
        }