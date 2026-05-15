from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel

#PERFIL DEL USUARIO RELACION UNO A UNO CON USER NATIVO DE DJANGO
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil"
    )
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    foto = models.ImageField(upload_to="perfiles/clientes/", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "perfiles_usuario"
        ordering = ["usuario__last_name", "usuario__first_name"]
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"{self.usuario.last_name}, {self.usuario.first_name}"

    @property
    def nombre_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

#PERFIL DEL VETERINARIO RELACION UNO A UNO CON USER NATIVO DE DJANGO

class VeterinarioPerfil(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil_veterinario"
    )
    matricula = models.CharField(max_length=50, unique=True)
    especialidad = models.CharField(max_length=120, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to="perfiles/veterinarios/", blank=True, null=True)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "veterinarios_perfiles"
        ordering = ["usuario__last_name", "usuario__first_name"]
        verbose_name = "Perfil Veterinario"
        verbose_name_plural = "Perfiles Veterinarios"

    def __str__(self):
        return f"{self.usuario.last_name}, {self.usuario.first_name}"

    @property
    def nombre_completo(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

#HORARIOS DE LOS VETERINARIOS RELACION MUCHOS A UNO CON VETERINARIO

# usuarios/models.py

class HorarioVeterinario(BaseModel):
    class DiaSemana(models.IntegerChoices):
        LUNES = 1, "Lunes"
        MARTES = 2, "Martes"
        MIERCOLES = 3, "Miércoles"
        JUEVES = 4, "Jueves"
        VIERNES = 5, "Viernes"
        SABADO = 6, "Sábado"
        DOMINGO = 7, "Domingo"

    veterinario = models.ForeignKey(
        VeterinarioPerfil, on_delete=models.CASCADE, related_name="horarios"
    )
    dia_semana = models.PositiveSmallIntegerField(choices=DiaSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = "horarios_veterinarios"
        ordering = ["veterinario", "dia_semana", "hora_inicio"]
        verbose_name = "Horario Veterinario"
        verbose_name_plural = "Horarios Veterinarios"

    def __str__(self):
        return f"{self.veterinario} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"