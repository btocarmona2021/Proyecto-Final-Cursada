# importo Serializer de rest_framework para crear serializers para los modelos Servicio y Turno.
from rest_framework import serializers

# importo los modelos Servicio y Turno para crear serializers basados en ellos.
from .models import Servicio, Turno

# importo serializers de Mascota y Veterinario para incluir información relacionada en el serializer de Turno.
from mascotas.serializers import MascotaSerializer

# importo el serializer de Veterinario para incluir información del veterinario en el serializer de Turno.
from usuarios.serializers import VeterinarioPerfilSerializer

# importo timedelta y timezone para validar que no haya turnos solapados para el mismo veterinario.
from datetime import timedelta, timezone as dt_timezone

# importo timezone de django para manejar zonas horarias en la validación de turnos solapados.
from django.utils import timezone


# SERIALIZERS PARA EL MODELO SERVICIO
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            "id",
            "nombre",
            "descripcion",
            "precio",
            "duracion_estimada",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# SERIALIZERS PARA EL MODELO DE CREACIÓN Y ACTUALIZACIÓN DE TURNOS, CON VALIDACIÓN DE HORARIOS SOLAPADOS
class TurnoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = [
            "id",
            "fecha_hora",
            "mascota",
            "veterinario",
            "servicio",
            "estado",
            "motivo_consulta",
            "notas",
            "creado_por_cliente",
            "urgencia",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        "Validar que no haya turnos duplicados para el mismo veterinario"
        # Obtengo los valores de veterinario, fecha_hora, servicio y urgencia del nuevo turno
        # o de la instancia existente (en caso de actualización).
        veterinario = data.get(
            "veterinario", getattr(self.instance, "veterinario", None)
        )
        fecha_hora = data.get("fecha_hora", getattr(self.instance, "fecha_hora", None))
        servicio = data.get("servicio", getattr(self.instance, "servicio", None))
        urgencia = data.get("urgencia", getattr(self.instance, "urgencia", False))

        # Si falta alguno de los datos necesarios para validar (veterinario, fecha_hora o servicio),
        # no hago la validación de solapamiento.
        if not veterinario or not fecha_hora or not servicio:
            return data
        # Si el turno es de urgencia, no hago la validación de solapamiento,
        # ya que los turnos de urgencia pueden solaparse.
        if urgencia:
            return data
        # Si es una actualización, comparo la nueva fecha_hora, veterinario y servicio con los valores anteriores.
        if self.instance:
            fecha_nueva_utc = (
                fecha_hora.astimezone(dt_timezone.utc)
                if fecha_hora.tzinfo
                else timezone.make_aware(fecha_hora).astimezone(dt_timezone.utc)
            )
            # Convierto la fecha_hora anterior a UTC para compararla con la nueva fecha_hora en UTC, evitando problemas de zonas horarias.
            fecha_vieja_utc = self.instance.fecha_hora.astimezone(dt_timezone.utc)
            # Verifico si hubo cambios en la fecha_hora, veterinario o servicio. Si no hubo cambios, no hago la validación de solapamiento.
            cambio_fecha = fecha_nueva_utc != fecha_vieja_utc
            cambio_vet = self.instance.veterinario_id != (
                veterinario.id if hasattr(veterinario, "id") else veterinario
            )
            # Verifico si hubo cambios en el servicio comparando el ID del servicio nuevo con el ID del servicio anterior. Si no hubo cambios, no hago la validación de solapamiento.
            cambio_servicio = self.instance.servicio_id != (
                servicio.id if hasattr(servicio, "id") else servicio
            )
            # Si no hay cambios en la fecha_hora, veterinario o servicio, no hago la validación de solapamiento.
            if not (cambio_fecha or cambio_vet or cambio_servicio):
                return data

        duracion = timedelta(minutes=servicio.duracion_estimada)
        fecha_hora_fin = fecha_hora + duracion
        # Busco turnos del mismo veterinario que se solapen con el nuevo turno, excluyendo los turnos de urgencia.
        turnos_conflicto = (
            Turno.objects.filter(
                veterinario=veterinario,
                urgencia=False,
            )
            .exclude(fecha_hora__gte=fecha_hora_fin)
            .exclude(fecha_hora__lt=fecha_hora - duracion)
        )
        # Si es una actualización, excluyo el turno actual de la búsqueda de conflictos.
        if self.instance and self.instance.pk:
            turnos_conflicto = turnos_conflicto.exclude(pk=self.instance.pk)
        # Si encuentro turnos que se solapan, lanzo un error de validación indicando que el veterinario tiene otro turno en ese horario.
        if turnos_conflicto.exists():
            raise serializers.ValidationError(
                {
                    "fecha_hora": "El veterinario tiene otro turno que se solapa con este horario."
                }
            )
        # Si no hay conflictos, retorno los datos validados.
        return data


# SERIALIZER PARA EL MODELO DE TURNO CON INFORMACIÓN RELACIONADA DE MASCOTA, 
# VETERINARIO Y SERVICIO, Y CAMPOS CALCULADOS COMO NOMBRES Y HORA DE FIN ESTIMADA.
class TurnoSerializer(serializers.ModelSerializer):
    # Traigo información relacionada de la mascota, veterinario y servicio utilizando serializers anidados y campos fuente para mostrar nombres e información detallada sin necesidad de hacer consultas adicionales en el frontend.
    mascota_info = MascotaSerializer(source="mascota", read_only=True)
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    mascota_id = serializers.IntegerField(source="mascota.id", read_only=True)
    veterinario_info = VeterinarioPerfilSerializer(source="veterinario", read_only=True)
    veterinario_nombre = serializers.SerializerMethodField()
    veterinario_id = serializers.IntegerField(source="veterinario.id", read_only=True)

    servicio_info = ServicioSerializer(source="servicio", read_only=True)
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)
    servicio_id = serializers.IntegerField(source="servicio.id", read_only=True)

    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    dueno_nombre = serializers.SerializerMethodField()
    hora_fin = serializers.SerializerMethodField()

    class Meta:
        model = Turno
        fields = [
            "id",
            "fecha_hora",
            "mascota_id",
            "mascota_nombre",
            "mascota_info",
            "veterinario_id",
            "veterinario_nombre",
            "veterinario_info",
            "servicio_id",
            "servicio_nombre",
            "servicio_info",
            "estado",
            "estado_display",
            "motivo_consulta",
            "notas",
            "creado_por_cliente",
            "dueno_nombre",
            "hora_fin",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = [
            "id",
            "mascota_id",
            "mascota_nombre",
            "mascota_info",
            "veterinario_id",
            "veterinario_nombre",
            "veterinario_info",
            "servicio_id",
            "servicio_nombre",
            "servicio_info",
            "estado_display",
            "dueno_nombre",
            "hora_fin",
            "created_at",
            "updated_at",
        ]

    def get_veterinario_nombre(self, obj):
        if obj.veterinario:
            u = obj.veterinario.usuario
            return f"{u.first_name} {u.last_name}".strip()
        return None

    def get_dueno_nombre(self, obj):
        if obj.mascota and obj.mascota.usuario:
            u = obj.mascota.usuario
            return f"{u.first_name} {u.last_name}".strip()
        return None

    def get_hora_fin(self, obj):
        """Calcula la hora de finalización del turno"""
        if obj.servicio and obj.servicio.duracion_estimada:
            hora_fin = obj.fecha_hora + timedelta(
                minutes=obj.servicio.duracion_estimada
            )
            return hora_fin.isoformat()
        return None
