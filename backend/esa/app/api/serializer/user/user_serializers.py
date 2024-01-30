from rest_framework import serializers

from esa.app.helpers.utils.validation_utils import ValidationUtils
from esa.app.models import UserEntity
from esa.app.models.entities.entities import GroupEntity
from esa.app.models.enums import SplitType


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
        fields = ["email", "first_name", "last_name", "id"]

class AddFriendRequestSerializer(serializers.Serializer):
    phone_number_or_email = serializers.CharField(required=True)

class FriendSerializer(serializers.Serializer):
    friend = UserSerializer()
    money_owed = serializers.IntegerField()

class FriendsSerializer(serializers.Serializer):
    friends = FriendSerializer(many=True)

class GetFriendExpensesRequestSerializer(serializers.Serializer):
    friend_id = serializers.UUIDField(required=False)

class CreateGroupRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    created_by = UserSerializer()

    class Meta:
        model = GroupEntity
        exclude = ["created_at", "is_deleted"]

class GroupListSerializer(serializers.Serializer):
    groups = GroupSerializer(many=True)

class AddGroupMemberRequestSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(required=True)
    user_id = serializers.UUIDField(required=True)


class AddFriendExpenseRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(max_length=1024)
    amount = serializers.IntegerField()
    paid_by = serializers.UUIDField(required=True)
    other_user = serializers.UUIDField(required=True)
    split_type = serializers.ChoiceField(choices=SplitType.choices)
    payer_amount = serializers.IntegerField(required=False)
    other_amount = serializers.IntegerField(required=False)
    payer_percentage = serializers.IntegerField(required=False)
    other_percentage = serializers.IntegerField(required=False)

    def validate(self, data):
        data_dict = dict(data)
        data_keys = data.keys()
        split_type = data_dict.get('account_type')
        if split_type == 'EXACT' and (('payer_amount' not in data_keys) or ('other_amount' not in data_keys)):
            raise serializers.ValidationError(
                'payer_amount and other_amount are required when split_type is exact.'
            )
        if split_type == 'PERCENTAGE' and (('payer_percentage' not in data_keys) or ('other_percentage' not in data_keys)):
            raise serializers.ValidationError(
                'payer_percentage and other_percentage are required when split_type is exact.'
            )
        return data
