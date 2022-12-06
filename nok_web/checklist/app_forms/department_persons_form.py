from django import forms
from nok_web.checklist.app_models.department_persons import Department_Persons


class Department_PersonsForm(forms.ModelForm):
    class Meta:
        model = Department_Persons
        fields = ['first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'department', 'is_deleted']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'second_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'position': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'department': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }