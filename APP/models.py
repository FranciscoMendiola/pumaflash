from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, unique=True)
    img_url = models.ImageField(upload_to='img/usuarios', default='img/usuarios/default.png')
    username = models.CharField(max_length=1, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'first_name', 'last_name', 'password','is_staff']
    
    def __str__(self):
        return self.email


class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    img_url = models.ImageField(upload_to='img/grupos', default='img/grupos/default.png')

    def __str__(self):
        return self.nombre + " - " + self.codigo

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()

    class Meta:
        unique_together = ('id_grupo', 'id_usuario')

    def __str__(self):
        return self.id_usuario.name + " - " + self.id_grupo.nombre

class Comentario(models.Model): 
    id_comentario = models.AutoField(primary_key=True)
    id_remitente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comentarios_enviados')
    id_destinatario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comentarios_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_remitente.id_usuario.name + " - " + self.id_destinatario.id_usuario.name