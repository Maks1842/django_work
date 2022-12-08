from django import forms
from nok_web.checklist.app_models.answers import Answers


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