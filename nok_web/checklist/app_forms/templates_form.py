from django import forms
from nok_web.checklist.app_models.templates import Templates


class TemplatesForm(forms.ModelForm):
    class Meta:
        model = Templates
        fields = ['name', 'type_organisations', 'template_file', 'version', 'is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'type_organisations': forms.Select(attrs={"class": "form-control"}),
            'template_file': forms.TextInput(attrs={"class": "form-control"}),
            'version': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }