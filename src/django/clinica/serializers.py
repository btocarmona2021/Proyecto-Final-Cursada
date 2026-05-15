from rest_framework import serializers
from .models import Veterinaria

# SERIALIZER PARA DATOS DE LA CLINICA
class VeterinariaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Veterinaria
        fields="__all__"
        read_only_fields=[
            "id",
            "created_at",
            "updated_at",
        ]
