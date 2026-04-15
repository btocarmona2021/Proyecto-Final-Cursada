from rest_framework import serializers
from .models import Rol, Usuario, Mascota, Servicio, Turno, HistorialMedico


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


# class UsuarioSerializer(serializers.ModelSerializer):
#     rol_nombre = serializers.CharField(source="rol.nombre", read_only=True)
#     password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = Usuario
#         fields = [
#             "id",
#             "nombre",
#             "apellido",
#             "email",
#             "password",
#             "telefono",
#             "direccion",
#             "rol",
#             "rol_nombre",
#             "especialidad",
#             "disponible",
#             "fecha_registro",
#             "activo",
#         ]

#     def create(self, validated_data):
#         password = validated_data.pop("password", None)
#         usuario = Usuario(**validated_data)
#         if password:
#             usuario.set_password(password)
#         usuario.save()
#         return usuario

#     def update(self, instance, validated_data):
#         password = validated_data.pop("password", None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         if password:
#             instance.set_password(password)
#         instance.save()
#         return instance


# class MascotaSerializer(serializers.ModelSerializer):
#     usuario_nombre = serializers.CharField(source="usuario.__str__", read_only=True)
#     sexo_display = serializers.CharField(source="get_sexo_display", read_only=True)

#     class Meta:
#         model = Mascota
#         fields = [
#             "id",
#             "nombre",
#             "especie",
#             "raza",
#             "fecha_nacimiento",
#             "sexo",
#             "sexo_display",
#             "color",
#             "peso",
#             "usuario",
#             "usuario_nombre",
#             "fecha_registro",
#         ]


# class ServicioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Servicio
#         fields = "__all__"


# class TurnoSerializer(serializers.ModelSerializer):
#     mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
#     veterinario_nombre = serializers.CharField(
#         source="veterinario.__str__", read_only=True
#     )
#     servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)
#     estado_display = serializers.CharField(source="get_estado_display", read_only=True)

#     class Meta:
#         model = Turno
#         fields = [
#             "id",
#             "fecha_hora",
#             "mascota",
#             "mascota_nombre",
#             "veterinario",
#             "veterinario_nombre",
#             "servicio",
#             "servicio_nombre",
#             "estado",
#             "estado_display",
#             "notas",
#             "fecha_creacion",
#         ]


# class HistorialMedicoSerializer(serializers.ModelSerializer):
#     mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
#     veterinario_nombre = serializers.CharField(
#         source="veterinario.__str__", read_only=True
#     )

#     class Meta:
#         model = HistorialMedico
#         fields = [
#             "id",
#             "mascota",
#             "mascota_nombre",
#             "fecha",
#             "veterinario",
#             "veterinario_nombre",
#             "diagnostico",
#             "tratamiento",
#             "observaciones",
#             "peso_actual",
#             "proxima_visita",
#         ]
