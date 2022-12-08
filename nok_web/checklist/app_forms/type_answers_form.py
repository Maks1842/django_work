from django import forms
from nok_web.checklist.app_models.type_answers import Type_Answers


class Type_AnswersForm(forms.ModelForm):
    class Meta:
        model = Type_Answers
        fields = ['type']
        widgets = {
            'type': forms.Select(attrs={"class": "form-control"}),
        }