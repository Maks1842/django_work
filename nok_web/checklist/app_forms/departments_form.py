from django import forms
from nok_web.checklist.app_models.departments import Departments


class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['department_name', 'address', 'phone', 'website', 'email', 'parent', 'region',
                  'type_departments', 'is_deleted', 'user']
        widgets = {
            'department_name': forms.TextInput(attrs={"class": "form-control"}),
            'address': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'website': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'parent': forms.Select(attrs={"class": "form-control"}),
            'region': forms.Select(attrs={"class": "form-control"}),
            'type_departments': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"})
        }