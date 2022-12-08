from django import forms
from nok_web.checklist.app_models.type_departments import Type_Departments


class Type_DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Type_Departments
        fields = ['type', 'is_deleted']
        widgets = {
            'type': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }