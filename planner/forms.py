from django import forms
from .models import Client, File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'date', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'cute-input w-full'}),
            'email': forms.EmailInput(attrs={'class': 'cute-input w-full'}),
            'phone': forms.TextInput(attrs={'class': 'cute-input w-full'}),
            'address': forms.Textarea(attrs={'class': 'cute-input w-full', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'cute-input w-full', 'rows': 3}),
        }