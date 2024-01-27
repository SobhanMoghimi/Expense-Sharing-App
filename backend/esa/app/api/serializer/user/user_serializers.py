from rest_framework import serializers

from esa.app.helpers.utils.validation_utils import ValidationUtils


class CustomerLoginRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserRegisterRequestSerializer(serializers.Serializer):
    email = serializers.CharField(validators=[ValidationUtils.validate_email])
    phone_number = serializers.CharField(validators=[ValidationUtils.validate_phone_number])
    first_name = serializers.CharField(required=True, validators=[ValidationUtils.validate_first_and_last_name])
    last_name = serializers.CharField(required=True, validators=[ValidationUtils.validate_first_and_last_name])
    password = serializers.CharField(validators=[ValidationUtils.validate_password], required=True)


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
    message = serializers.CharField(required=False)

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
