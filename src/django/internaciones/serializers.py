from rest_framework import serializers
from .models import Internacion, EvolucionInternacion

# SERIALIZER PARA INTERNACION
class InternacionSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.SerializerMethodField()
    veterinario_nombre = serializers.SerializerMethodField()
    estado_display = serializers.SerializerMethodField()

    class Meta:
        model = Internacion
        fields = [
            "id",
            "mascota",
            "mascota_nombre",
            "veterinario_responsable",  # ✅ CORREGIDO
            "veterinario_nombre",
            "fecha_ingreso",
            "fecha_egreso",
            "motivo",
            "diagnostico_ingreso",  # ✅ CORREGIDO
            "observaciones",
            "estado",
            "estado_display",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = [
            "id",
            "mascota_nombre",
            "veterinario_nombre",
            "estado_display",
            "created_at",
            "updated_at",
        ]

    def get_mascota_nombre(self, obj):
        return obj.mascota.nombre if obj.mascota_id else None

    def get_veterinario_nombre(self, obj):
        if obj.veterinario_responsable_id:  # ✅ CORREGIDO
            u = obj.veterinario_responsable.usuario
            return f"{u.last_name}, {u.first_name}".strip()
        return None

    def get_estado_display(self, obj):
        return obj.get_estado_display()


# SERIALIZER PARA EVOLUCION DE INTERNACION
class EvolucionInternacionSerializer(serializers.ModelSerializer):
    internacion_info = serializers.SerializerMethodField()
    veterinario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = EvolucionInternacion
        fields = [
            "id",
            "internacion",
            "internacion_info",  # ✅ Info completa
            "veterinario",
            "veterinario_nombre",
            "fecha",
            "temperatura",
            "peso",
            "descripcion",
            "indicaciones",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = [
            "id",
            "internacion_info",
            "veterinario_nombre",
            "created_at",
            "updated_at",
        ]

    def get_internacion_info(self, obj):
        if obj.internacion:
            return {
                "id": obj.internacion.id,
                "mascota_nombre": obj.internacion.mascota.nombre,
                "mascota_id": obj.internacion.mascota_id,
                "motivo": obj.internacion.motivo,
                "estado": obj.internacion.get_estado_display(),
            }
        return None

    def get_veterinario_nombre(self, obj):
        if obj.veterinario_id:
            u = obj.veterinario.usuario
            return f"{u.last_name}, {u.first_name}".strip()
        return None