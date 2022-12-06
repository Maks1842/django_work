from django import forms
# from .models import Category         # для работы с Формами, НЕ связанные с Моделями
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

