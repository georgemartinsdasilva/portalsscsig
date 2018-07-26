from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from usuario.models import Perfil
from django.forms import ModelForm

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['Setor', 'Gestor','funcao','num_tel','first_name','last_name', 'perm']