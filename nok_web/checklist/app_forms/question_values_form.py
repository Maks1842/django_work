from django import forms
from nok_web.checklist.app_models.question_values import Question_Values


class Question_ValuesForm(forms.ModelForm):
    class Meta:
        model = Question_Values
        fields = ['value_name', 'name_alternativ']
        widgets = {
            'value_name': forms.TextInput(attrs={"class": "form-control"}),
            'name_alternativ': forms.TextInput(attrs={"class": "form-control"}),
        }