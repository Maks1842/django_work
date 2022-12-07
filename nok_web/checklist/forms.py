from django import forms
# from .models import Category         # для работы с Формами, НЕ связанные с Моделями
from .models import *                  # для работы с Формами, связанные с Моделями
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# from .app_models.recommendations import Recommendations


# class UserLoginForm(AuthenticationForm):
#     username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#
# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(max_length=150, label='Имя пользователя',
#           help_text='Подсказка: максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(max_length=50, label='Пароль',
#           widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(max_length=50, label='Подтверждение пароля',
#           widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class RegionsForm(forms.ModelForm):
    class Meta:
        model = Regions
        fields = ['region_name', 'is_deleted']
        widgets = {
            'region_name': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class Type_DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Type_Departments
        fields = ['type', 'is_deleted']
        widgets = {
            'type': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


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


class Type_OrganisationsForm(forms.ModelForm):
    class Meta:
        model = Type_Organisations
        fields = ['type', 'is_deleted']
        widgets = {
            'type': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class OrganisationsForm(forms.ModelForm):
    class Meta:
        model = Organisations
        fields = ['organisation_name', 'address', 'phone', 'website', 'email', 'parent', 'department', 'quota', 'is_deleted']
        widgets = {
            'organisation_name': forms.TextInput(attrs={"class": "form-control"}),
            'address': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'website': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'parent': forms.Select(attrs={"class": "form-control"}),
            'department': forms.Select(attrs={"class": "form-control"}),
            'quota': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class Form_Type_OrganisationForm(forms.ModelForm):
    class Meta:
        model = Form_Type_Organisation
        fields = ['organisation', 'type_organisation']
        widgets = {
            'organisation': forms.Select(attrs={"class": "form-control"}),
            'type_organisation': forms.Select(attrs={"class": "form-control"})
        }


class Organisation_PersonsForm(forms.ModelForm):
    class Meta:
        model = Organisation_Persons
        fields = ['first_name', 'second_name', 'last_name', 'position', 'phone', 'email', 'is_deleted']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'second_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'position': forms.TextInput(attrs={"class": "form-control"}),
            'phone': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class Form_Organisation_PersonsForm(forms.ModelForm):
    class Meta:
        model = Form_Organisation_Persons
        fields = ['organisation', 'person']
        widgets = {
            'organisation': forms.Select(attrs={"class": "form-control"}),
            'person': forms.Select(attrs={"class": "form-control"})
        }


class QuotaForm(forms.ModelForm):
    class Meta:
        model = Quota
        fields = ['quota']
        widgets = {
            'quota': forms.TextInput(attrs={"class": "form-control"}),
        }


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


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['questions']
        widgets = {
            'questions': forms.TextInput(attrs={"class": "form-control"}),
        }


class Question_ValuesForm(forms.ModelForm):
    class Meta:
        model = Question_Values
        fields = ['value_name', 'name_alternativ']
        widgets = {
            'value_name': forms.TextInput(attrs={"class": "form-control"}),
            'name_alternativ': forms.TextInput(attrs={"class": "form-control"}),
        }


class Form_Sections_QuestionForm(forms.ModelForm):
    class Meta:
        model = Form_Sections_Question
        fields = ['question', 'order_num', 'form_sections', 'type_answers', 'answer_variant', 'type_organisations', 'is_deleted']
        widgets = {
            'question': forms.Select(attrs={"class": "form-control"}),
            'order_num': forms.TextInput(attrs={"class": "form-control"}),
            'form_sections': forms.Select(attrs={"class": "form-control"}),
            'type_answers': forms.Select(attrs={"class": "form-control"}),
            'answer_variant': forms.TextInput(attrs={"class": "form-control"}),
            'type_organisations': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


# class RecommendationsForm(forms.ModelForm):
#     class Meta:
#         model = Recommendations
#         fields = ['name', 'is_deleted']
#         widgets = {
#             'name': forms.TextInput(attrs={"class": "form-control"}),
#             'is_deleted': forms.Select(attrs={"class": "form-control"})
#         }


class Forms_RecommendationsForm(forms.ModelForm):
    class Meta:
        model = Forms_Recommendations
        fields = ['free_value', 'answers', 'form_sections', 'recommendations', 'is_deleted']
        widgets = {
            'free_value': forms.TextInput(attrs={"class": "form-control"}),
            'answers': forms.Select(attrs={"class": "form-control"}),
            'form_sections': forms.Select(attrs={"class": "form-control"}),
            'recommendations': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['organisations', 'type_organisations', 'checking', 'answers_json', 'is_deleted']
        widgets = {
            'organisations': forms.Select(attrs={"class": "form-control"}),
            'type_organisations': forms.Select(attrs={"class": "form-control"}),
            'checking': forms.Select(attrs={"class": "form-control"}),
            'answers_json': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class Signed_DociumentsForm(forms.ModelForm):
    class Meta:
        model = Signed_Dociuments
        fields = ['file_name', 'originat_file_name', 'description', 'created_at', 'is_deleted', 'user']
        widgets = {
            'file_name': forms.TextInput(attrs={"class": "form-control"}),
            'originat_file_name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
            'created_at': forms.DateInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"})
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['free_value', 'is_deleted']
        widgets = {
            'free_value': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file_name', 'original_file_name', 'description', 'created_at', 'is_deleted', 'user']
        widgets = {
            'file_name': forms.TextInput(attrs={"class": "form-control"}),
            'original_file_name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
            'created_at': forms.DateInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"})
        }


class VersionsForm(forms.ModelForm):
    class Meta:
        model = Versions
        fields = ['table_name', 'version', 'active', 'is_deleted']
        widgets = {
            'table_name': forms.TextInput(attrs={"class": "form-control"}),
            'version': forms.TextInput(attrs={"class": "form-control"}),
            'active': forms.Select(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }


class Type_AnswersForm(forms.ModelForm):
    class Meta:
        model = Type_Answers
        fields = ['type']
        widgets = {
            'type': forms.Select(attrs={"class": "form-control"}),
        }


class Transaction_ExchangeForm(forms.ModelForm):
    class Meta:
        model = Transaction_Exchange
        fields = ['model', 'field', 'old_data', 'new_data', 'user']
        widgets = {
            'model': forms.Select(attrs={"class": "form-control"}),
            'field': forms.Select(attrs={"class": "form-control"}),
            'old_data': forms.Select(attrs={"class": "form-control"}),
            'new_data': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"}),
        }



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

