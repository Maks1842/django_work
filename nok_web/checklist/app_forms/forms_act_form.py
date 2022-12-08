from django import forms
from ..app_models.forms_act import FormsAct


class FormsActForm(forms.ModelForm):
    class Meta:
        model = FormsAct
        fields = ['type_departments', 'type_organisations', 'act_json', 'date', 'version']
        widgets = {
            'type_departments': forms.Select(attrs={"class": "form-control"}),
            'type_organisations': forms.Select(attrs={"class": "form-control"}),
            'act_json': forms.Textarea(attrs={"class": "form-control", "rows": 17}),
            'date': forms.DateInput(attrs={"class": "form-control"}),
            'version': forms.TextInput(attrs={"class": "form-control"}),
        }