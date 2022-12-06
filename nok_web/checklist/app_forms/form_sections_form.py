from django import forms
from nok_web.checklist.app_models.form_sections import Form_Sections


class Form_SectionsForm(forms.ModelForm):
    class Meta:
        model = Form_Sections
        fields = ['name', 'version', 'order_num', 'parent', 'type_departments', 'is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'version': forms.TextInput(attrs={"class": "form-control"}),
            'order_num': forms.TextInput(attrs={"class": "form-control"}),
            'parent': forms.Select(attrs={"class": "form-control"}),
            'type_departments': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }