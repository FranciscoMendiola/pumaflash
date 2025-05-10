from django import forms
from APP.models import User  # Asegúrate de que el modelo se llama 'User'


class UserForm(forms.ModelForm):
    '''
    Formulario basado en el modelo User para la creación de un usuario
    '''
    # Campo adicional agregado al formulario para la confirmación de la contraseña
    username = forms.CharField(widget=forms.TextInput(),
                               label="Nombres(s)", required=True)
    first_name = forms.CharField(
        widget=forms.TextInput(), label="Apellido paterno", required=True)
    last_name = forms.CharField(
        widget=forms.TextInput(), label="Apellido materno", required=True)
    email = forms.CharField(widget=forms.EmailInput(),
                            label="Correo", required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Contraseña", required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label="Confirmar Contraseña", required=True)
    img_url = forms.CharField(widget=forms.FileInput(),
                              label="Imagen de perfil", required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password', 'confirm_password', 'img_url']
        labels = {'username': 'Nombre(s)', 'first_name': 'Apellido Paterno', 'last_name': 'Apellido Materno',
                  'email': 'Correo', 'password': 'Contraseña',
                  'img_url': 'Imagen de Perfil'}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if password:
            if len(password) < 6:
                raise forms.ValidationError(
                    "La contraseña debe tener al menos 6 caracteres.")

        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo ya está registrado.")

        return cleaned_data


class LoginForm(forms.Form):
    '''
    Formulario para obtener las credenciales de inicio de sesión de un usuario
    '''
    email = forms.EmailField(widget=forms.EmailInput(),
                             label="Correo", required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Contraseña", required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not email:
            raise forms.ValidationError("Ingrese un correo.")

        if "@" not in email:  # Validación básica de formato de correo
            raise forms.ValidationError("Correo no válido.")

        # Verifica si el correo está registrado
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo no está registrado.")

        return cleaned_data
