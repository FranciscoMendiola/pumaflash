from django.contrib.auth.decorators import login_required
import random, string  # Esto debe estar importado para usar en generar_codigo_unico
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
                request.session['usuario_id'] = usuario.id_usuario
                # Redirección por rol
                if usuario.is_admin:
                    return redirect('generator')
                else:
                    return redirect('groups')
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

def groups(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()

        try:
            grupo = Grupo.objects.get(codigo=code)
            messages.success(request, 'Código válido. Acceso concedido.')
            return redirect('prueba', nombre=grupo.nombre)  
        except Grupo.DoesNotExist:
            messages.error(request, 'Código inválido. Verifica con tu profesor.')

    return render(request, 'groups.html')

def generar_codigo_unico():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Grupo.objects.filter(codigo=codigo).exists():
            return codigo

def generator(request):
    codigo_generado = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')  # debe venir del form

        if nombre and descripcion:
            codigo = generar_codigo_unico()
            nuevo = Grupo(
                nombre=nombre,
                descripcion=descripcion,
                codigo=codigo,
                id_admin= request.user #-------------------> No me jala esto por algo de como se define el id admin unu
            )
            nuevo.save()
            codigo_generado = codigo

    codigos = Grupo.objects.all().order_by('-id_grupo')

    return render(request, 'generator.html', {
        'codigo_generado': codigo_generado,
        'codigos': codigos
    })

@login_required(login_url='/')  # o donde esté tu login
def redireccion_por_rol(request):
    if Grupo.objects.filter(id_admin=request.user).exists():
        return redirect('generator')
    else:
        return redirect('groups')

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