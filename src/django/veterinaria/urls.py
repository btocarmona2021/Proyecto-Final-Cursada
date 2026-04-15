from django.urls import path
from . import views

urlpatterns = [
    path('',views.inicio),
    path('adios',views.adios),
    path('datos/<str:nombre>/<str:desc>/<int:precio>/<int:duracion>',views.servicio)
]
