from django import forms
from nok_web.checklist.app_models.questions import Questions


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['questions']
        widgets = {
            'questions': forms.TextInput(attrs={"class": "form-control"}),
        }