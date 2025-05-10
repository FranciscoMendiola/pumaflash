
from django.shortcuts import render, redirect
from APP.models import User
import uuid
from APP.forms import UserForm, LoginForm
from django.http import HttpResponse


# Dependencias de Django
from django.contrib.auth import authenticate, login
from django.contrib import messages



# Create your views here.
def index(request):
    # login se pone como pestaña activa por defecto (luego si el registro da error esto cambia)
    data = {'user_form': UserForm(),'login_form': LoginForm(), 'active_tab': 'login'}

    if request.user.is_authenticated:
        # Si el usuario ya está autenticado, redirige a la página principal
        print(request.user.name)

    if request.method == "POST":
        tipoFormulario = request.POST.get("tipoFormulario") # Campo oculto en los html para distinguir de qué formulario viene la info
        if tipoFormulario == "login":
            return user_login(request,data)
        elif tipoFormulario == "register":
            return user_register(request, data)
        
    return render(request, 'index.html', data)

def user_login(request, data):
    form = LoginForm(request.POST)  # Crea el formulario con los datos POST
    
    if form.is_valid():  # Si el formulario es válido
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        # Usamos authenticate() para verificar si las credenciales son correctas
        user = authenticate(request, email=email, password=password)
        
        if user is not None:  # Si el usuario existe y las credenciales son correctas
            login(request, user)  # Autenticamos al usuario y lo logueamos automáticamente
            print("Login correcto, bienvenida ")
            return redirect("index")  # Redirige a la página principal (o a donde desees)
        else:
            messages.error(request, "Correo o contraseña incorrectos")
    
    else:
        # Si el formulario no es válido
        print("Formulario de login no válido")
    
    __get_first_error(form, request)  # Si hay errores, los muestra
    data["login_form"] = form  # Pasamos el formulario con errores a la vista
    data["active_tab"] = "login"  # Activa la pestaña de login en la interfaz
    return render(request, "index.html", data)  # Renderiza la página con los datos y el formulario

    
def user_register(request, data):
    form = UserForm(request.POST, request.FILES)  # Crea el formulario con los datos POST y archivos (como la imagen)
    
    if form.is_valid():  # Si el formulario es válido
        user = form.save(commit=False)  # No guarda inmediatamente el usuario en la base de datos
        
        user.set_password(form.cleaned_data['password'])  # Establece la contraseña cifrada
        user.save()  # Guarda el usuario en la base de datos
        messages.success(request, "Registro exitoso")  # Mensaje de éxito
        
    else:
        # Si el formulario no es válido, muestra el primer error
        __get_first_error(form, request)  
        data["user_form"] = form  # Pasamos el formulario con errores a la vista
        data["active_tab"] = "register"  # Activa la pestaña de registro en la interfaz

        print("Formulario de registro no válido")
        print(form.errors)  # Imprime los errores del formulario en la consola
    
    return render(request, "index.html", data)  # Renderiza la página con los datos y el formulario



# Función privada para obtener el primer mensaje de error del formulario
def __get_first_error(form, request):
    # Primero buscar errores de campo
    for field_name, field_errors in form.errors.items():
        if field_errors:
            label = form.fields.get(field_name).label if field_name in form.fields else ""
            message = f"{label}: {field_errors[0]}" if label else field_errors[0]
            messages.error(request, message)
            return message
    # Si no hay errores de campo, buscar errores no asociados
    if form.non_field_errors():
        message = form.non_field_errors()[0]
        messages.error(request, message)
        return message
    return None

def verificar_sesion_navegador(request):

    user_agent_actual = request.META.get('HTTP_USER_AGENT', '')
    user_agent_guardado = request.session.get('user_agent', '')

    if user_agent_guardado and user_agent_guardado != user_agent_actual:
        return ("Estás en otro navegador")
    
    return ("Estás en el mismo navegador")
