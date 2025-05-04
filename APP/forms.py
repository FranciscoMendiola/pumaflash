from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # Excluimos el id_usuario para que no se muestre en el formulario
        exclude = ['id_usuario']
        # También puedes usar fields si prefieres enumerarlos explícitamente
        # fields = ['nombre', 'apellido_materno', 'apellido_paterno', 'correo', 'password', 'img_url', 'is_admin']
        widgets = {
            'password': forms.PasswordInput(),
        }