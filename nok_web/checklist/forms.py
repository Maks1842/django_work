from django import forms
# from .models import Category    # для работы с Формами, НЕ связанные с Моделями
from .models import Department    # для работы с Формами, связанные с Моделями
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Department
        #field = '__all__'         # Если нужно все поля из Модели добавить в форму (не рекомендуется)
        fields = ['name_of_department', 'address', 'tel', 'website', 'email', 'fio_responsible', 'region_id']
        widgets = {
            'name_of_department': forms.TextInput(attrs={"class": "form-control"}),
            'address': forms.TextInput(attrs={"class": "form-control"}),
            'tel': forms.TextInput(attrs={"class": "form-control"}),
            'website': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'fio_responsible': forms.TextInput(attrs={"class": "form-control"}),
            'region_id': forms.Select(attrs={"class": "form-control"})
        }
