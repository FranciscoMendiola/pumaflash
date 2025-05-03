
from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.

'''
numCnta|   nombres      |   apellidos   |    grupos   |
-------------------------------------------------------
  314  |    César       |    Jardines   | 1 (id_grupo)|
'''
def index(request):
    return HttpResponse("Hello, World!")

def tontines(re):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 33
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Hurtado Aponte Joshua Abel,Felipe Ramírez Alondra Navila, Flores Muñoz Mauricio, Mendiola Montes Victor Manuel")

def cums(request):
    '''
    1.- Todos los estudiantes con nombres Victor Manuel
    2.- Todos los estudiantes con numCta 320
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Perez Aparicio Ariadna Beatriz, Garcia Gommez Eduardo Biali")

def ejercicio1(request):
    '''
    1.- Todos los estudiantes con nombres Moisés
    2.- Todos los estudiantes con numCta 318
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Levi Iparrea, Vazquez Jose, Barradas Alberto")

def equipo_n(request):
    '''
    1.- Todos los estudiantes con apellidos Martínez
    2.- Todos los estudiantes con numCta 42
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Alcantara Andrade Daniel, Rodriguez Nevarez Edwin, Sanchez Rosas Roberto Samuel, Cataneo Tortolero Andres Rodrigo")

def ekiposupercool(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 33
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("López Asano Miguel Akira, Martínez Marcelo Ingrid Aylen, Pérez Evristo Eris, Ramírez Venegas Alexa Paola")
    
def space4(request):
    '''
    1.- Todos los estudiantes con nombres Victor Manuel
    2.- Todos los estudiantes con numCta 320
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("del Valle Vera Nancy Elena, Ugalde Flores Jimena, Cruz Gonzalez Irvin Javie")

def Dinamita(requestt):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 319
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Maro Flores Cid, Etni Sarai Castro Sierra, Moises Corpus Garcia, Moises Abraham Lira Rivera")

def ekuipo(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 319
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Castillo Camacho Violeta Ardeni, \n Juarez Cruz Joshua\n Kevin Steve Quezada Ordoñez\n karla Clemente Herrera") 

def Labubusalvajes(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 33
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Alan Oliver Lopez Robles, Dylan Enrique Juarez Martinez")  

def indez(request):
    '''
    1.- Todos los estudiantes con nombres Victor Manuel
    2.- Todos los estudiantes con numCta 320
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Luis Gerardo Estrada Garcia, Luis Ernesto Hernandez Rosas, Uziel Vidal Cruz, Yuznhio Sierra Casiano")

def index1(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 319
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Antonio Castillo Hernandez, Sergio Mejia Caballero, Ixchel Velazquez Vilchis")

def foo(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 319
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Ramón Arcos Morales, Victor Manuel Casarrubias Casarrubias")

def us(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 33
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("'Mildred, Leslie, Aldo, Francisco'")

def equipoPerdido1(request):
    '''
    1.- Todos los estudiantes con nombres Victor Manuel
    2.- Todos los estudiantes con numCta 320
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Luis Ernesto Hernández Rosas, Luis Gerardo, Yuznhio, Uziel Vidal")

def URLEquipo(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 319
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Ixchell, Atonio, Sergio")

def ekipo(request):
    '''
    1.- Todos los estudiantes
    2.- Todos los estudiantes con numCta 319
    3.- Los integrantes de este equipo
    '''
    return HttpResponse("Itzel, Raúl, Josue")