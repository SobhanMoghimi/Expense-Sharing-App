import json
from _decimal import Decimal
from uuid import UUID

from django.db.models import QuerySet

from esa.app.helpers.exceptions.exceptions import AlreadyExistsException
from esa.app.models import UserEntity
from esa.app.models.entities.entities import GroupEntity


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

    def add_friend(self, user: UserEntity, friend_user: UserEntity):
        if friend_user in user.friends.all():
            AlreadyExistsException("User already exists.")
        user.friends.add(friend_user)
        user.save()