from django import forms
from nok_web.checklist.app_models.type_organisations import Type_Organisations


class Type_OrganisationsForm(forms.ModelForm):
    class Meta:
        model = Type_Organisations
        fields = ['type', 'is_deleted']
        widgets = {
            'type': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }