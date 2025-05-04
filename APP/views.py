
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
    return HttpResponse("Hello, World!")


def Signup(request):
    data = {'form': UsuarioForm()}
    
    if request.method == "POST":
        formulario = UsuarioForm(request.POST, request.FILES)
        if formulario.is_valid():
            usuario = formulario.save()
            messages.success(request, "Registro exitoso")
            return redirect("signup")
        else:
            print(formulario.errors) 
        data["form"] = formulario

    return render(request, 'registration/registration.html', data)

