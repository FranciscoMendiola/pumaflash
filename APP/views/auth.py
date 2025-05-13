
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from APP.forms import UserForm,LoginForm  # Import UserForm from the forms module
from django.contrib.auth import authenticate, login

class AuthView(View):
    '''
    Vista para manejar el registro y login de usuarios
    '''
    def get(self, request):
        # Si el usuario ya está autenticado, redirige a la página principal
        if request.user.is_authenticated:
            return redirect("home", "qwerty")
        
        data = {'user_form': UserForm(), 'login_form': LoginForm(), 'active_tab': 'login'}

        return render(request, 'index.html', data)
    
    def post(self, request):
        data = {'user_form': UserForm(), 'login_form': LoginForm(), 'active_tab': 'login'}
        # Campo oculto en los html para distinguir de qué formulario viene la info
        tipoFormulario = request.POST.get("tipoFormulario")
        if tipoFormulario == "login":
            return self.__user_login(request, data)
        elif tipoFormulario == "register":
            return self.__user_register(request, data)
        else:
            # Si no se reconoce el formulario, redirige a la página principal
            return redirect("auth")
    
    def __user_login(self, request, data):
        form = LoginForm(request.POST)
        # Si el formulario es válido
        if form.is_valid():
            email = form.cleaned_data['email']

            password = form.cleaned_data['password']
            # Usamos authenticate() para verificar si las credenciales son correctas
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Autenticamos al usuario y lo logueamos automáticamente
                login(request, user)
                print("Login correcto, bienvenido(a) ")
                # Redirige a la página principal (o a donde desees)
                return redirect("home", "qwerty")
            else:
                messages.error(request, "Correo o contraseña incorrectos")
        else:
            # Si el formulario no es válido
            print("Formulario de login no válido")
            # Si hay errores, obtiene el primero
            self.__get_first_error(request, form)

        # Pasamos el formulario con errores a la vista
        data['login_form'] = form
        # Renderiza la página con los datos y el formulario
        return render(request, "index.html", data)

    def __user_register(self, request, data):
        form = UserForm(request.POST, request.FILES)
        # Si el formulario es válido
        if form.is_valid():
            # Guardamos el usuario en la base de datos
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Usuario registrado correctamente")
            data['active_tab'] = 'login'
            form = UserForm()
        else:
            # Si el formulario no es válido
            print("Formulario de registro no válido")
            # Si hay errores, los muestra
            self.__get_first_error(request, form)
            # Pasamos el formulario con errores a la vi
            data['active_tab'] = 'register'
        
        data['user_form'] = form
        # Renderiza la página con los datos y el formulario
        return render(request, "index.html", data)

    # Función privada para obtener el primer mensaje de error del formulario
    def __get_first_error(self, request, form):
        # Primero buscar errores de campo
        for field_name, field_errors in form.errors.items():
            if field_errors:
                label = form.fields.get(
                    field_name).label if field_name in form.fields else ""
                message = f"{label}: {field_errors[0]}" if label else field_errors[0]
                messages.error(request, message)
                return message
        # Si no hay errores de campo, buscar errores no asociados
        if form.non_field_errors():
            message = form.non_field_errors()[0]
            messages.error(request, message)
            return message
        return None