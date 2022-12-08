from django import forms
from nok_web.checklist.app_models.list_checking import List_Checking


class ListCheckingForm(forms.ModelForm):
    class Meta:
        model = List_Checking
        fields = ['checking', 'organisation', 'user', 'is_deleted']
        widgets = {
            'checking': forms.Select(attrs={"class": "form-control"}),
            'organisation': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"}),
        }