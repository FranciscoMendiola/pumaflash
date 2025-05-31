from django import forms
from django.contrib.auth import authenticate
# Asegúrate de que el modelo se llama 'User'
from APP.models import Profile, User, Comment


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


class ProfileEditForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Nombre(s)",required=True)
    first_name = forms.CharField(widget=forms.TextInput(), label="Apellido paterno",required=True)
    last_name = forms.CharField(widget=forms.TextInput(), label="Apellido materno",required=True)
    description = forms.CharField(widget=forms.Textarea(), label="Descripción",required=True)
    current_password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña actual",required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), label="Nueva contraseña",required=False)
    img_url = forms.ImageField(label="Imagen de perfil",required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Guardar el usuario actual para validaciones

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')

        # Validar contraseña actual si se proporciona una nueva contraseña
        if new_password:
            if not current_password:
                raise forms.ValidationError({'current_password': 'Ingresa tu contraseña actual para confirmar el cambia de contraseña.'})
            # Verificar que la contraseña actual sea correcta
            if not self.user or not authenticate(email=self.user.email, password=current_password):
                raise forms.ValidationError({'current_password': 'La contraseña actual es incorrecta.'})
            # Validar la nueva contraseña (ejemplo: longitud mínima)
            if len(new_password) < 6:
                raise forms.ValidationError({'new_password': 'La nueva contraseña debe tener al menos 6 caracteres.'})

        # Validar que se proporcione la contraseña actual si se intenta cambiar la contraseña
        if current_password and not new_password:
            raise forms.ValidationError({'new_password': 'Debes ingresar una nueva contraseña si proporcionas la contraseña actual.'})

        # Validar la imagen (opcional, si se sube)
        img_url = cleaned_data.get('img_url')
        if img_url:
            # Validar tipo de archivo (solo imágenes)
            if not img_url.content_type.startswith('image/'):
                raise forms.ValidationError({'img_url': 'El archivo debe ser una imagen válida (jpg, png, etc.).'})

        return cleaned_data