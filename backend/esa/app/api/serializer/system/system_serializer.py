from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status_code = serializers.IntegerField()
