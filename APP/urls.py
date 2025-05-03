from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("equipo_n/", views.equipo_n, name="equipo_n"),
    path("ekiposupercool/", views.ekiposupercool, name ="ekiposupercool"),
    path("ekuipo/", views.ekuipo, name="ekuuipo"),        
    path("Space4Equipo/", views.space4, name="space4"),
    path("equipoDinamita/", views.ejercicio1, name="Dinamita"),
    path("Labubusalvaje/", views.Labubusalvajes, name="Labubusalvaje"),
    path("cums/", views.cums, name="Cumis"),
    path("tontines/", views.tontines, name="Tonotos"),
    path("equipofoo/", views.foo, name="foo"),
    path("equipous/", views.us, name="us"),
    path("MiPrimerURL/", views.indez, name="zedni"),
    path("equipoPerdido1/", views.equipoPerdido1, name="equipoPerdido1"),
    path("URL/", views.URLEquipo, name="url"),
    path("ekipo/", views.ekipo, name="equipoPerdido1")
 ]

