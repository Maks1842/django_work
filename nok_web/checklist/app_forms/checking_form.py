
from django import forms
from nok_web.checklist.app_models.checking import Checking


class CheckingForm(forms.ModelForm):
    class Meta:
        model = Checking
        fields = ['name', 'date_checking', 'region', 'department', 'is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'date_checking': forms.DateInput(attrs={"class": "form-control"}),
            'region': forms.Select(attrs={"class": "form-control"}),
            'department': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"}),
        }