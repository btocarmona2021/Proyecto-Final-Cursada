from django.contrib.auth.models import User
from django.db import models
from core.models import BaseModel

#MODELO ESPECIE

class Especie(BaseModel):
    nombre= models.CharField(max_length=100,unique=True)
    emoji = models.CharField(max_length=10,blank=True,null=True)
    
    class Meta:
        db_table="especies"
        ordering = ["nombre"]
        verbose_name = "Especie"
        verbose_name_plural= "Especies"

    def __str__(self):
        return f"{self.nombre}"

#MODELO RAZA

class Raza(BaseModel):

    #RELACION CON ESPECIE
    especie = models.ForeignKey(Especie,on_delete=models.CASCADE,related_name="razas")

    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "razas"
        ordering = ["especie__nombre", "nombre"]
        verbose_name = "Raza"
        verbose_name_plural="Razas"
        unique_together = ("especie","nombre")

    def __str__(self):
        return f"{self.nombre}({self.especie.nombre})"
    
#MODELO MASCOTA

class Mascota(BaseModel):
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        HEMBRA ="H", "Hembra"

    #RELACIONES CON RAZA Y USUARIO
    raza = models.ForeignKey(Raza,on_delete=models.PROTECT,related_name="mascotas")
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,related_name="mascotas")

    nombre = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    peso_actual = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    microchip = models.CharField(max_length=50, unique=True, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to="mascotas/", blank=True, null=True)

    class Meta:
        db_table = "mascotas"
        ordering=["nombre"]
        verbose_name= "Mascota"
        verbose_name_plural = "Mascotas"
    
    def __str__(self):
        return f"{self.nombre}-{self.usuario.get_full_name() or self.usuario.username}"
    