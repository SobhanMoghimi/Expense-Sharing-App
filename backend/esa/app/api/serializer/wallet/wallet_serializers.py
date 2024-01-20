from _decimal import Decimal

from rest_framework import serializers

from mmb.app.models.entities.address_entities import WalletAddressesEntity, TransactionEntity
from mmb.app.models.enums import TxType


class DepositRequestSerializer(serializers.Serializer):
    private_key = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=36, decimal_places=18, min_value=Decimal("0.0000000000000000001"), required=True)
    wallet_address = serializers.CharField(required=True)

class CreateAddressRequestSerializer(serializers.Serializer):
    number_of_addresses = serializers.IntegerField(min_value=1, required=False, default=1)
    address_index_start = serializers.IntegerField(min_value=1, required=False, default=1)
    mnemonic = serializers.CharField()

class WalletAddressSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    address_index = serializers.IntegerField(min_value=1)
    public_key = serializers.CharField(max_length=256)
    wallet_address = serializers.CharField(max_length=256)
    bnb_address_balance = serializers.DecimalField(max_digits=36, decimal_places=18)
    token_address_balance = serializers.DecimalField(max_digits=36, decimal_places=18)


class GetAddressOutputSerializer(serializers.Serializer):
    addresses = WalletAddressSerializer(many=True)

class PaginatedAddressResponse(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = WalletAddressSerializer(many=True)

class TransactionSerializer(serializers.ModelSerializer):
    wallet_address = serializers.SerializerMethodField()

    class Meta:
      model =TransactionEntity
      fields =("created_at", "tx_hash", "task_type", "tx_type", "wallet_address")


    def get_wallet_address(self, obj):
        return obj.wallet_address.wallet_address

class GetTransactionsOutputSerializer(serializers.Serializer):
    transactions = TransactionSerializer(many=True)

class PaginatedTransactionResponse(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = TransactionSerializer(many=True)

class PaginatedRequest(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=20)