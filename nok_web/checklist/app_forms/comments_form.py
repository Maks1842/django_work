from django import forms
from nok_web.checklist.app_models.comments import Comments


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['free_value', 'is_deleted']
        widgets = {
            'free_value': forms.TextInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"})
        }