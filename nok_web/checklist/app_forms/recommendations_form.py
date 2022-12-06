from django import forms
from nok_web.checklist.app_models.recommendations import Recommendations


class RecommendationsForm(forms.ModelForm):
    class Meta:
        model = Recommendations
        fields = ['name', 'id_type_departments', 'id_questions', 'is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'id_type_departments': forms.TextInput(attrs={"class": "form-control"}),
            'id_questions': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }