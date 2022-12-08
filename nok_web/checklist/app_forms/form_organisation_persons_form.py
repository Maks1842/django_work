from django import forms
from nok_web.checklist.app_models.form_organisation_persons import Form_Organisation_Persons


class Form_Organisation_PersonsForm(forms.ModelForm):
    class Meta:
        model = Form_Organisation_Persons
        fields = ['organisation', 'person']
        widgets = {
            'organisation': forms.Select(attrs={"class": "form-control"}),
            'person': forms.Select(attrs={"class": "form-control"})
        }