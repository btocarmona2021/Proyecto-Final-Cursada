from django.db import models
from core.models import BaseModel

class Veterinaria(BaseModel):
    razon_social = models.CharField(max_length=200)
    nombre_fantasia = models.CharField(max_length=200, blank=True, null=True)
    cuit = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="veterinaria/", blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    horario_atencion = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Veterinaria"
        verbose_name = "Veterinaria"
        verbose_name_plural = "Veterinaria"
        
    def __str__(self):
        return self.razon_social
    
    def save(self,*args, **kwargs):
        if not self.pk and Veterinaria.objects.exists():
            raise ValueError("Solo se permite registrar una Veterinaria")
        super().save(*args,**kwargs)
        

    
