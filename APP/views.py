
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
        else:
            #Tipo de formulario no reconocido llega al index de nuevo
            return render(request, 'index.html', data)
        
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
        return redirect("index")
    else:
        data["form"] = formulario
        data["active_tab"] = "register"
        return render(request, "index.html", data)
    
    


