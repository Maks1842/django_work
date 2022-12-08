from django import forms
from nok_web.checklist.app_models.forms_recommendations import Forms_Recommendations


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