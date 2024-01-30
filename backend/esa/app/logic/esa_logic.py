import time
from _decimal import Decimal
from uuid import UUID

from django.db.models import QuerySet
from rest_framework_simplejwt.tokens import RefreshToken

from esa.app.adapters.postgres_adapter import PostgresAdapter
from esa.app.helpers.exceptions.exceptions import UserWithPasswordNotFoundException, AlreadyExistsException, \
    UserNotFoundException
from esa.app.helpers.metaclasses.singleton import Singleton
from esa.app.models import UserEntity
from esa.app.models.dtos.dtos import LoginDTO, LogoutDto, TokenDTO
from esa.app.models.entities.entities import GroupEntity


class ExpenseSharingAPPLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.db_adapter = PostgresAdapter()

    def register(self, first_name: str, last_name: str, email: str, phone_number: str, password: str) -> TokenDTO:
        if user := self.db_adapter.get_user_by_email(email):
            raise AlreadyExistsException("User already exists.")
        if phone_number:
            if user:= self.db_adapter.get_user_by_phone_number(phone_number):
                raise AlreadyExistsException("User already exists.")

        user = self.db_adapter.add_user(first_name, last_name , email, phone_number, password)
        access_token, refresh_token = self.create_tokens(user=user)

        return TokenDTO(access_token=str(access_token), refresh_token=str(access_token))

    def login(self, validated_dto: LoginDTO):
        customer = self.db_adapter.get_user_by_email(validated_dto.email)
        if not customer:
            raise UserWithPasswordNotFoundException()
        if customer.check_password(validated_dto.password):
            access_token, refresh_token = self.create_tokens(user=customer)

            return {"access_token": str(access_token), "refresh_token": str(refresh_token)}
        else:
            raise UserWithPasswordNotFoundException()

    def create_tokens(self, user: UserEntity):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return access_token, refresh_token

    def logout(self, logout_dto: LogoutDto) -> None:
        token = RefreshToken(logout_dto.refresh_token)
        token.blacklist()

    def create_group(self, user: UserEntity, group_name: str, group_description: str) -> GroupEntity:
        return self.db_adapter.create_group(user, group_name, group_description)

    def get_user_groups(self, user: UserEntity) -> QuerySet[GroupEntity]:
        return self.db_adapter.get_user_groups(user)

    def add_group_member(self, user: UserEntity, group_id: UUID, user_id: UUID) -> GroupEntity:
        if not (added_user := self.db_adapter.get_user_by_id(user_id)):
            raise UserNotFoundException()
        # TODO: CHECK FRIENDSHIP
        self.db_adapter.add_group_member()

    def add_friend(self, user: UserEntity, phone_or_email: str) -> None:
        if friend_user := self.db_adapter.get_user_by_email(phone_or_email):
            self.db_adapter.add_friend(user, friend_user)
        elif friend_user:= self.db_adapter.get_user_by_phone_number(phone_or_email):
            self.db_adapter.add_friend(user, friend_user)
        else:
            raise UserNotFoundException()

    def get_friends(self, user: UserEntity) -> list[(UserEntity, int)]:
        return self.db_adapter.get_friends(user)

    def test(self):
        print("WAH")
        token_price = self.bsc_adapter.get_token_price()
        self.buy_token_and_wait_for_mining(Decimal("0.00001"), token_price)
        # self.sell_token_and_wait_for_mining(Decimal("0.00001"), price)
        # token_amount = (Decimal("0.00001") / token_price).quantize(Decimal("0.000000000000000001"))
        # address = WalletDTO.model_validate(self.choose_address_to_sell(token_amount))
        # self.update_address_balances(address)
        print("Woah")
