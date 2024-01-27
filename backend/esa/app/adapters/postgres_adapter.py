import json
from _decimal import Decimal

from django.db.models import QuerySet

from esa.app.models import UserEntity
from esa.app.models.entities.entities import GroupEntity


class PostgresAdapter:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_user_by_email(email: str) -> UserEntity:
        return UserEntity.objects.filter(email=email).first()

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> UserEntity:
        return UserEntity.objects.filter(phone_number=phone_number).first()

    @staticmethod
    def add_user(first_name: str, last_name: str, email: str, phone_number: str, password: str) -> UserEntity:
        return UserEntity.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )

    @staticmethod
    def create_group(user: UserEntity, group_name: str, group_description: str) -> GroupEntity:
        return GroupEntity.objects.create(
            name=group_name,
            description=group_description,
            created_by=user,
            members=[user]
        )
