from django.db import models

# Create your models here.
class Grupo (models.Model):
    id_grupo = models.AutoField(primary_key=True)

class Estudiante (models.Model):
    numCta = models. IntegerField (default=0)
    nombres = models. CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    # Aqui guardamos los grupos de un alumno
    grupos = models.ManyToManyField (Grupo, blank=True)


