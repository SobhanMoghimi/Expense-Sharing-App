from rest_framework import serializers

from esa.app.helpers.utils.validation_utils import ValidationUtils
from esa.app.models import UserEntity
from esa.app.models.entities.entities import GroupEntity


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        include = ["email", "first_name", "last_name", "id"]

class AddFriendRequestSerializer(serializers.Serializer):
    phone_number_or_email = serializers.CharField(required=True)

class FriendSerializer(serializers.Serializer):
    friend = UserSerializer()
    money_owed = serializers.IntegerField()

class FriendsSerializer(serializers.Serializer):
    friends_with_owed = FriendSerializer(many=True)

class CreateGroupRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupEntity
        exclude = []

class GroupListSerializer(serializers.Serializer):
    groups = GroupSerializer(many=True)

class AddGroupMemberRequestSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)

