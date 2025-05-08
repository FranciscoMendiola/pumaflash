from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('redireccion/', views.redireccion_por_rol, name='redireccion'),
    path('groups/', views.groups, name='groups'),
    path('generator/', views.generator, name='generator'),
 ]