from django.shortcuts import render
from django.http import HttpResponse
from veterinaria.models import Servicio
def inicio(request):
    return HttpResponse('<h1>Hola Mundo<h1/>')

def adios(request):
    return HttpResponse('<h1>Adios<h1/>')

def servicio(request,nombre,desc,precio,duracion):
    serv = Servicio(nombre=nombre,descripcion=desc,precio=precio,duracion_estimada=duracion)
    serv.save()
    return HttpResponse('Servicio Creado')
