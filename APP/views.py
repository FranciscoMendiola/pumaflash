
from django.shortcuts import HttpResponse
from django.shortcuts import render
from APP.models import Usuario
from django.core.files import File


# Create your views here.
def index(request):

    # Crea un nuevo usuario (o usa uno existente)
    usuario = Usuario(nombre="Juan", apellido_materno="Pérez", apellido_paterno="Gómez", correo="juan@example.com", password="12345")

    # Asigna la imagen
    with open('/home/francisco/Imágenes/LOGO_COREWAVE.png', 'rb') as f:
        usuario.img_url.save('gt.png', File(f), save=True)

    # Guarda el usuario
    usuario.save()

    # Verifica
    print(usuario.img_url.url)  # Debería mostrar algo como '/media/img/usuarios/gt.png'
    return HttpResponse("Hello, World!")