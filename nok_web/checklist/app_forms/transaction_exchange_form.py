from django import forms
from nok_web.checklist.app_models.transaction_exchange import Transaction_Exchange


class Transaction_ExchangeForm(forms.ModelForm):
    class Meta:
        model = Transaction_Exchange
        fields = ['model', 'field', 'old_data', 'new_data', 'user']
        widgets = {
            'model': forms.Select(attrs={"class": "form-control"}),
            'field': forms.Select(attrs={"class": "form-control"}),
            'old_data': forms.Select(attrs={"class": "form-control"}),
            'new_data': forms.Select(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control"}),
        }