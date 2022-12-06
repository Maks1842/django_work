from django import forms
from nok_web.checklist.app_models.photo import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file_name', 'original_file_name', 'description', 'created_at', 'is_deleted', 'user']
        widgets = {
            'file_name': forms.TextInput(attrs={"class": "form-control"}),
            'original_file_name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.TextInput(attrs={"class": "form-control"}),
            'created_at': forms.DateInput(attrs={"class": "form-control"}),
            'is_deleted': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"})
        }