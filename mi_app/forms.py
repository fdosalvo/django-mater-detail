
        
        
        
from django import forms
from .models import Header

class HeaderForm(forms.ModelForm):
    class Meta:
        model = Header
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'start_date', 'name': 'start_date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'end_date', 'name': 'end_date'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'id': 'description', 'name': 'description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity', 'name': 'quantity'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'id': 'message', 'name': 'message'}),
        }