from rest_framework import serializers


class CustomerLoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
    message = serializers.CharField(required=False)

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
