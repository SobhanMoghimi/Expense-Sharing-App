import json
from _decimal import Decimal

from django.db.models import QuerySet

from esa.app.models import UserEntity


class PostgresAdapter:
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_user_by_email(email: str) -> UserEntity:
        return UserEntity.objects.filter(email=email).first()

    # @staticmethod
    # def get_auth_token(self, token: str) -> auth:
