from django import forms
from nok_web.checklist.app_models.organisation_persons import Organisation_Persons


class Organisation_PersonsForm(forms.ModelForm):
    class Meta:
        model = Organisation_Persons
        fields = ['first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'is_deleted']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'second_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'position': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }