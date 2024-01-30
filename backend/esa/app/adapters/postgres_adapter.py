import json
from _decimal import Decimal
from uuid import UUID

from django.db.models import QuerySet

from esa.app.helpers.exceptions.exceptions import AlreadyExistsException
from esa.app.models import UserEntity
from esa.app.models.entities.entities import GroupEntity, FriendshipEntity


class PostgresAdapter:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_user_by_email(email: str) -> UserEntity:
        return UserEntity.objects.filter(email=email).first()

    @staticmethod
    def get_user_by_id(user_id: UUID) -> UserEntity:
        return UserEntity.objects.filter(id=user_id).first()

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> UserEntity:
        return UserEntity.objects.filter(phone_number=phone_number).first()

    @staticmethod
    def add_user(first_name: str, last_name: str, email: str, phone_number: str, password: str) -> UserEntity:
        user = UserEntity.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def create_group(user: UserEntity, group_name: str, group_description: str) -> GroupEntity:
        group = GroupEntity.objects.create(
            name=group_name,
            description=group_description,
            created_by=user,
        )
        group.members.add(user)
        group.save()
        return group


    @staticmethod
    def get_user_groups(user: UserEntity) -> QuerySet[GroupEntity]:
        return GroupEntity.objects.filter(members=user)

    def add_friend(self, user: UserEntity, friend_user: UserEntity) -> None:
        if FriendshipEntity.objects.filter(user=user, friend_user=friend_user):
            AlreadyExistsException("User already exists in your friend list.")
        if user.id == friend_user.id:
            raise Exception("Can't add yourself to your friends.")
        FriendshipEntity.objects.create(user=user, friend_user=friend_user)


    @staticmethod
    def get_friends(user: UserEntity) -> list[(UserEntity, int)]:
        friendships = FriendshipEntity.objects.filter(user=user)
        return [{'friend': friendship.friend_user, 'money_owed': friendship.money_owed} for friendship in friendships]