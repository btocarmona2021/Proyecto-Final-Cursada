from rest_framework import serializers
from core.imagenes import ImagenValidada
from .models import Veterinaria

# SERIALIZER PARA DATOS DE LA CLINICA
class VeterinariaSerializer(serializers.ModelSerializer):
    logo = ImagenValidada(required=False, allow_null=True)

    def validate(self, data):
        if self.instance is None and Veterinaria.objects.exists():
            raise serializers.ValidationError(
                'La clínica ya está registrada. Editá sus datos en lugar de crear otra.'
            )
        return data

    class Meta:
        model=Veterinaria
        fields="__all__"
        read_only_fields=[
            "id",
            "created_at",
            "updated_at",
        ]
