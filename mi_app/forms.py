from django import forms
from .models import Header

class HeaderForm(forms.ModelForm):
    class Meta:
        model = Header
        fields = ['start_date', 'end_date', 'description', 'quantity', 'message']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }