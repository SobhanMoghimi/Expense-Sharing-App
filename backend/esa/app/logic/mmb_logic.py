import time
from _decimal import Decimal

from django.db.models import QuerySet
from rest_framework_simplejwt.tokens import RefreshToken

from esa.app.adapters.postgres_adapter import PostgresAdapter
from esa.app.helpers.exceptions.exceptions import UserNotFoundException
from esa.app.helpers.metaclasses.singleton import Singleton
from esa.app.models import UserEntity
from esa.app.models.dtos.dtos import LoginDTO, LogoutDto


class MarketMakerLogic(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.db_adapter = PostgresAdapter()

    def login(self, validated_dto: LoginDTO):
        customer = self.db_adapter.get_user_by_email(validated_dto.email)
        if not customer:
            raise UserNotFoundException()
        if customer.check_password(validated_dto.password):
            access_token, refresh_token = self.create_tokens(customer=customer)

            return {"access_token": str(access_token), "refresh_token": str(refresh_token)}
        else:
            raise UserNotFoundException()

    def create_tokens(self, customer: UserEntity):
        refresh_token = RefreshToken.for_user(customer)
        access_token = refresh_token.access_token
        return access_token, refresh_token

    def logout(self, logout_dto: LogoutDto) -> None:
        token = RefreshToken(logout_dto.refresh_token)
        token.blacklist()

    def test(self):
        print("WAH")
        token_price = self.bsc_adapter.get_token_price()
        self.buy_token_and_wait_for_mining(Decimal("0.00001"), token_price)
        # self.sell_token_and_wait_for_mining(Decimal("0.00001"), price)
        # token_amount = (Decimal("0.00001") / token_price).quantize(Decimal("0.000000000000000001"))
        # address = WalletDTO.model_validate(self.choose_address_to_sell(token_amount))
        # self.update_address_balances(address)
        print("Woah")
