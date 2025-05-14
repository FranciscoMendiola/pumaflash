from django import forms
# Asegúrate de que el modelo se llama 'User'
from APP.models import User, Comment


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


class StudentSearchForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(
    ), label="Nombres(s):", max_length=100, required=False)
    first_name = forms.CharField(widget=forms.TextInput(
    ), label="Apellido paterno", max_length=100, required=False)
    last_name = forms.CharField(widget=forms.TextInput(
    ), label="Apellido paterno", max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


class CommentForm(forms.ModelForm):
    '''
    Formulario basado en el modelo Comment para la creación de un comentario
    '''

    class Meta:
        model = Comment
        fields = ['content']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")

        if content:
            if len(content) < 1:
                raise forms.ValidationError(
                    "El comentario no puede estar vacío.")

        return cleaned_data
