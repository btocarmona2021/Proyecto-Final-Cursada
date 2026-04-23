from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# MODELO BASE PARA REUTILIZAR Y HEREDAR EN OTROS MNODELOS
class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Veterinaria(BaseModel):  # ← hereda BaseModel
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
        db_table = "veterinaria"
        verbose_name = "Veterinaria"
        verbose_name_plural = "Veterinaria"

    def __str__(self):
        return self.razon_social

    def save(self, *args, **kwargs):
        if not self.pk and Veterinaria.objects.exists():
            raise ValueError("Solo se permite registrar una veterinaria.")
        super().save(*args, **kwargs)


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


class Especie(BaseModel):
    nombre = models.CharField(max_length=80, unique=True)
    emoji = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "especies"
        ordering = ["nombre"]
        verbose_name_plural = "Especies"

    def __str__(self):
        return self.nombre


class Raza(BaseModel):

    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, related_name="razas")
    nombre = models.CharField(max_length=120)
    

    class Meta:
        db_table = "razas"
        ordering = ["nombre"]
        unique_together = ("especie", "nombre")
        verbose_name_plural = "Razas"

    def __str__(self):
        return f"{self.nombre} ({self.especie.nombre})"


class Mascota(BaseModel):
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        HEMBRA = "H", "Hembra"

    raza = models.ForeignKey(Raza, on_delete=models.PROTECT, related_name="mascotas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mascotas")
    
    nombre = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, blank=True, null=True)
    color = models.CharField(max_length=80, blank=True, null=True)
    peso_actual = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    microchip = models.CharField(max_length=50, blank=True, null=True, unique=True)
    observaciones_generales = models.TextField(blank=True, null=True)
    
    
    fecha_registro = models.DateTimeField(default=timezone.now)
    foto = models.ImageField(upload_to="mascotas/", blank=True, null=True)

    class Meta:
        db_table = "mascotas"
        ordering = ["nombre"]
        verbose_name_plural = "Mascotas"

    def __str__(self):
        return self.nombre


class Servicio(BaseModel):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duracion_estimada = models.PositiveIntegerField(help_text="Duración en minutos")

    class Meta:
        db_table = "servicios"
        ordering = ["nombre"]
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


class Turno(BaseModel):
    class Estado(models.TextChoices):
        RESERVADO = "reservado", "Reservado"
        CONFIRMADO = "confirmado", "Confirmado"
        EN_ESPERA = "en_espera", "En espera"
        EN_CONSULTA = "en_consulta", "En consulta"
        ATENDIDO = "atendido", "Atendido"
        CANCELADO = "cancelado", "Cancelado"

    fecha_hora = models.DateTimeField()
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="turnos"
    )
    veterinario = models.ForeignKey(
        VeterinarioPerfil, on_delete=models.PROTECT, related_name="turnos_asignados"
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.PROTECT, related_name="turnos"
    )
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.RESERVADO
    )
    motivo_consulta = models.CharField(max_length=255, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    creado_por_cliente = models.BooleanField(default=False)

    class Meta:
        db_table = "turnos"
        ordering = ["fecha_hora"]
        verbose_name_plural = "Turnos"

    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha_hora}"


class ConsultaClinica(BaseModel):
    class TipoConsulta(models.TextChoices):
        CONTROL = "control", "Control general"
        VACUNACION = "vacunacion", "Vacunación"
        CIRUGIA = "cirugia", "Cirugía"
        URGENCIA = "urgencia", "Urgencia"
        POST_OPERATORIO = "post_operatorio", "Post-operatorio"
        DESPARASITACION = "desparasitacion", "Desparasitación"
        OTRO = "otro", "Otro"

    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="consultas"
    )
    turno = models.OneToOneField(
        Turno,
        on_delete=models.SET_NULL,
        related_name="consulta_clinica",
        null=True,
        blank=True,
    )
    fecha = models.DateTimeField(default=timezone.now)
    veterinario = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consultas_clinicas",
    )
    tipo = models.CharField(
        max_length=30, choices=TipoConsulta.choices, default=TipoConsulta.CONTROL
    )
    motivo_consulta = models.CharField(max_length=255, blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    peso_actual = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    frecuencia_cardiaca = models.PositiveIntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True)
    proxima_visita = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "consultas_clinicas"
        ordering = ["-fecha"]
        verbose_name = "Consulta Clínica"
        verbose_name_plural = "Consultas Clínicas"

    def __str__(self):
        return f"Consulta {self.id} - {self.mascota.nombre}"


class RecetaItem(BaseModel):
    consulta = models.ForeignKey(
        ConsultaClinica, on_delete=models.CASCADE, related_name="recetas"
    )
    medicamento = models.CharField(max_length=150)
    dosis = models.CharField(max_length=150)
    frecuencia = models.CharField(max_length=150, blank=True, null=True)
    dias = models.PositiveIntegerField(blank=True, null=True)
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "recetas_items"
        ordering = ["consulta", "id"]
        verbose_name = "Ítem de Receta"
        verbose_name_plural = "Ítems de Receta"

    def __str__(self):
        return f"{self.medicamento} - {self.consulta.mascota.nombre}"


class Vacuna(BaseModel):
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="vacunas"
    )
    nombre = models.CharField(max_length=120)
    fecha_aplicacion = models.DateField()
    fecha_proxima = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    veterinario = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vacunas_aplicadas",
    )

    class Meta:
        db_table = "vacunas"
        ordering = ["-fecha_aplicacion"]
        verbose_name_plural = "Vacunas"

    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre}"


class Internacion(BaseModel):
    class Estado(models.TextChoices):
        INTERNADO = "internado", "Internado"
        OBSERVACION = "observacion", "En observación"
        ALTA = "alta", "Alta médica"

    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="internaciones"
    )
    veterinario_responsable = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.PROTECT,
        related_name="internaciones_responsable",
    )
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_egreso = models.DateTimeField(blank=True, null=True)
    motivo = models.CharField(max_length=255)
    diagnostico_ingreso = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.INTERNADO
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "internaciones"
        ordering = ["-fecha_ingreso"]
        verbose_name = "Internación"
        verbose_name_plural = "Internaciones"

    def __str__(self):
        return f"Internación {self.mascota.nombre} - {self.fecha_ingreso}"


class EvolucionInternacion(BaseModel):
    internacion = models.ForeignKey(
        Internacion, on_delete=models.CASCADE, related_name="evoluciones"
    )
    fecha = models.DateTimeField(default=timezone.now)
    veterinario = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evoluciones_internacion",
    )
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    peso = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField()
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "evoluciones_internacion"
        ordering = ["-fecha"]
        verbose_name = "Evolución de Internación"
        verbose_name_plural = "Evoluciones de Internación"

    def __str__(self):
        return f"Evolución {self.internacion.mascota.nombre} - {self.fecha}"


class Notificacion(BaseModel):
    class Tipo(models.TextChoices):
        TURNO = "turno", "Turno"
        VACUNA = "vacuna", "Vacuna"
        INTERNACION = "internacion", "Internación"
        SISTEMA = "sistema", "Sistema"

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notificaciones"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "notificaciones"
        ordering = ["-fecha_creacion"]
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return self.titulo
