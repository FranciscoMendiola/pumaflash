from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario

class nameForm(forms.Form):
    '''
    Como los 3 son filtro entonces les agregamos la propiedad de que no sean obligatorios para hacer submit
    '''
    numcta = forms.CharField(label='numcta', max_length=100, required=False)
    nombre = forms.CharField(label='nombre', max_length=100, required=False)
    apellido = forms.CharField(label='apellido', max_length=100, required=False)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'password', 'img_url']
        widgets = {
            'password': forms.PasswordInput()
        }