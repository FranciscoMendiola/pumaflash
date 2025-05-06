from django.db import models

# Create your models here. pope francis
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    correo = models.EmailField(max_length=80, unique=True)
    contraseña = models.TextField()
    img_url = models.ImageField(upload_to='img/usuarios', default='img/usuarios/default.png')
    is_admin = models.BooleanField(default=False)

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    img_url = models.ImageField(upload_to='img/grupos', default='img/grupos/default.png')

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField()

    class Meta:
        unique_together = ('id_grupo', 'id_usuario')

class Comentario(models.Model): 
    id_comentario = models.AutoField(primary_key=True)
    id_remitente = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comentarios_enviados')
    id_destinatario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comentarios_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)