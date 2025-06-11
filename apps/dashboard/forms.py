from django import forms
from .models import Profile

#Controlador de nuestro formulario

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'phone', 'email', 'photo']

class EditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'name', 'phone', 'email']