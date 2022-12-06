from django import forms
from nok_web.checklist.app_models.form_sections_question import Form_Sections_Question


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