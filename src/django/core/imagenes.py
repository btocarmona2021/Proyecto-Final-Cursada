from rest_framework import serializers


class ImagenValidada(serializers.ImageField):
    """Imágenes raster verificadas por Pillow, hasta 5 MiB."""
    def to_internal_value(self, data):
        if getattr(data, 'size', 0) > 5 * 1024 * 1024:
            raise serializers.ValidationError('La imagen no puede superar los 5 MB.')
        archivo = super().to_internal_value(data)
        if archivo.image.format not in ('JPEG', 'PNG', 'WEBP'):
            raise serializers.ValidationError('Usá una imagen JPG, PNG o WebP.')
        return archivo
