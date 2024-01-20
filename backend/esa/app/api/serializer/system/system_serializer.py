from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status_code = serializers.IntegerField()

class GetTokenPriceSerializer(serializers.Serializer):
    price_in_bnb = serializers.DecimalField(max_digits=36, decimal_places=18)
