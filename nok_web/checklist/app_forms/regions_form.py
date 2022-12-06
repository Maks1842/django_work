from django import forms
from nok_web.checklist.app_models.regions import Regions


class RegionsForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ['region_name', 'is_deleted']
        widgets = {
            'region_name': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }