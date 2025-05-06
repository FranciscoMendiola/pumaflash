
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from APP.models import Usuario
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password,check_password #Biblioteca para usar contraseña hash

# Dependencias de Django
from django.core.files import File
from django.contrib.auth import authenticate, login
from django.contrib import messages
 


# Create your views here.
def index(request):
    # login se pone como pestaña activa por defecto (luego si el registro da error esto cambia)
    data = {'form': UsuarioForm(),'login_form': loginForm(), 'active_tab': 'login'}

    if request.method == "POST":
        tipoFormulario = request.POST.get("tipoFormulario") # Campo oculto en los html para distinguir de qué formulario viene la info
        if tipoFormulario == "login":
            return login(request,data)
        elif tipoFormulario == "register":
            return registro(request, data)
        
    return render(request, 'index.html', data)

def login(request, data):
    formulario = loginForm(request.POST)
    if formulario.is_valid():
        correo = formulario.cleaned_data['correo']
        contraseña = formulario.cleaned_data['contraseña']
        try:
            usuario = Usuario.objects.get(correo=correo)
            if check_password(contraseña, usuario.contraseña):
                
                ##################
                #Acá va a ir todo lo que viene después del login, podrían hacer un render pasando el usuario o sus datos yo q sé ahí le ven uds
                print("Login correcto, bienvenida ")
                print(usuario.nombre)                
                return redirect("index")
                ##############
            else:
                messages.error(request, "Contraseña incorrecta")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
    else:
        # Si el formulario no es correcto
        print("Formulario de login no válido")

    __get_first_error(formulario, request)
    # Re-renderizar el formulario con los errores de validación
    data["login_form"] = formulario
    data["active_tab"] = "login"
    return render(request, "index.html", data)
    
def registro(request, data):
    formulario = UsuarioForm(request.POST, request.FILES)
    if formulario.is_valid():
        usuario = formulario.save(commit=False)
        usuario.contraseña = make_password(formulario.cleaned_data['contraseña'])
        usuario.save()
        messages.success(request, "Registro exitoso")
    else:
        __get_first_error(formulario, request)
        data["form"] = formulario
        data["active_tab"] = "register"

    return render(request, "index.html", data)


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