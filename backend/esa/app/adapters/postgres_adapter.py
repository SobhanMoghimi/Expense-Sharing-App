import json
import math
from _decimal import Decimal
from uuid import UUID

from django.db.models import QuerySet

from esa.app.helpers.exceptions.exceptions import AlreadyExistsException
from esa.app.models import UserEntity
from esa.app.models.dtos.dtos import FriendExpenseDTO
from esa.app.models.entities.entities import GroupEntity, FriendshipEntity, ExpenseEntity, SplitEntity
from esa.app.models.enums import SplitType


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

    def get_or_create_friend(self, user: UserEntity, friend_user: UserEntity) -> FriendshipEntity:
        # if FriendshipEntity.objects.filter(user=user, friend_user=friend_user):
        #     AlreadyExistsException("User already exists in your friend list.")
        if user.id == friend_user.id:
            raise Exception("Can't add yourself to your friends.")
        return FriendshipEntity.objects.get_or_create(user=user, friend_user=friend_user)


    @staticmethod
    def get_friends(user: UserEntity) -> list[(UserEntity, int)]:
        friendships = FriendshipEntity.objects.filter(user=user)
        return [{'friend': friendship.friend_user, 'money_owed': friendship.money_owed} for friendship in friendships]

    def add_friend_equal_expense(self, expense_dto: FriendExpenseDTO) -> None:
        expense = self.add_friend_expense(expense_dto)
        SplitEntity.objects.create(
            user=expense_dto.paid_by,
            expense=expense,
            share=math.ceil(expense_dto.amount / 2),
            split_type=SplitType
        )
    def add_friend_exact_expense(self, expense_dto: FriendExpenseDTO) -> None:
        expense = self.add_friend_expense(expense_dto)
        SplitEntity.objects.create(
            user=expense_dto.paid_by,
            expense=expense,
            share=math.ceil(expense_dto.amount / 2),
            split_type=SplitType
        )

    def add_friend_percentage_expense(self, expense_dto: FriendExpenseDTO) -> None:
        expense = self.add_friend_expense(expense_dto)

    @staticmethod
    def add_friend_expense(expense_dto: FriendExpenseDTO) -> ExpenseEntity:
        return ExpenseEntity.objects.create(
            title=expense_dto.title,
            description=expense_dto.description,
            amount=expense_dto.amount,
            created_by=expense_dto.created_by,
            paid_by=expense_dto.paid_by,
        )
