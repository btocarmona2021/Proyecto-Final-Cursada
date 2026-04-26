from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenPersonalizado(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        grupos = self.user.groups.values_list("name", flat=True)
        data["grupo"] = grupos[0] if grupos else None
        return data
