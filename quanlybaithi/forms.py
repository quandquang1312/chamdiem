from django import forms
from .models import Baithi
from django.contrib.auth.models import User

class BaithiForm(forms.ModelForm):
    class Meta:
        model = Baithi
        fields = ('ten', 'created_by')
        
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'ten-form'}),
            'created_by': forms.TextInput(attrs={'class': 'create-form', 'value': '', 'id': 'author', 'type': 'hidden'}),
        }