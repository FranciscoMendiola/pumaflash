from django import forms
from .models import Usuario

# Bibliotecas del video de César
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    '''
    Formulario basado en el modelo Usuario para la creación de un usuario
    '''
    # Parámetro extra agregado al formulario un campo para contraseña 
    # (al usar el wideget PasswordInput() en el html se pondrá "censurada" por defecto, es decir de tipo password)
    confirma_contraseña = forms.CharField(widget=forms.PasswordInput(), label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'contraseña', 'confirma_contraseña', 'img_url']
        widgets = {
            'contraseña': forms.PasswordInput(),
        }

    def clean(self): 
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        if contraseña:
            # Validación de la contraseña (mínimo 8 caracteres, al menos una letra y un número)
            if len(contraseña) < 6:
                raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        confirma_contraseña = cleaned_data.get("confirma_contraseña")
        correo = cleaned_data.get("correo")

        if contraseña and confirma_contraseña and contraseña != confirma_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("El correo ya está registrado.")

class loginForm(forms.Form):
    '''
    Formulario para obtener los datos de inicio de sesión de un usuario
    '''
    correo = forms.EmailField(label="Correo", required=True)
    contraseña = forms.CharField(label="Contraseña", widget=forms.PasswordInput(), required=True)

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo:  # Validación personalizada
            raise forms.ValidationError("Por favor ingrese un correo.")
        if "@" not in correo:
            raise forms.ValidationError("El correo no tiene un formato válido.")
        return correo