from django import forms
from nok_web.checklist.app_models.recommendations import Recommendations


class RecommendationsForm(forms.ModelForm):
    class Meta:
        model = Recommendations
        fields = ['name', 'is_deleted']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }