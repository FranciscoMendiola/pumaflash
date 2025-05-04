
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from APP.models import Usuario
from .models import *
from .forms import *

# Dependencias de Django
from django.core.files import File
from django.contrib.auth import authenticate, login
from django.contrib import messages
 


# Create your views here.
def index(request):

    # Crea un nuevo usuario (o usa uno existente)
    #usuario = Usuario(nombre="Juan", apellido_materno="Pérez", apellido_paterno="Gómez", correo="juan@example.com", password="12345")

    # Asigna la imagen
    #with open('E:\Descargas\Vmod.png', 'rb') as f:
    #    usuario.img_url.save('gt.png', File(f), save=True)

    # Guarda el usuario
    #usuario.save()

    # Verifica
    #print(usuario.img_url.url)  # Debería mostrar algo como '/media/img/usuarios/gt.png'
    return HttpResponse("Hello, World!")


def Signup(request):
    '''
    Función de registro de usuario de tipo estudiante
    '''
    data = {
        'form': UsuarioForm()
    }
    if request.method == "POST":
        print(request.FILES)  # Agrega esto
        formulario = UsuarioForm(request.POST, request.FILES)
        if formulario.is_valid():
            usuario = formulario.save()  # Solo se guarda una vez
            messages.success(request, "Registro exitoso")
            return redirect("index")
        data["form"] = formulario
    return render(request, 'registration/registration.html', data)
        