from typing import Any

from rest_framework import status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'
    default_code = 'not_found'


class CommonsBaseException(Exception):
    ...


class InvalidUrlException(CommonsBaseException):
    def __init__(self, url: str):
        super().__init__(f"Invalid url format for {url}")


class InvalidEntityTypeException(TypeError):
    def __init__(self, entity: Any, type_: type | list[type]):
        super().__init__(f"INAPPROPRIATE ARGUMENT TYPE, {entity} MUST BE INHERITED FROM {type_}")


class DefinitionException(CommonsBaseException):
    def __init__(self, message: str | None = None):
        super().__init__(message)


class ProviderConnectionException(CommonsBaseException):
    def __init__(self):
        super().__init__("provider rpc network exception")


class LowAddressBalanceException(CommonsBaseException):
    def __init__(self):
        super().__init__("Address balance is lower than expected amount for deposits")


class UserNotFoundException(NotFound):
    def __init__(self):
        super().__init__()
        self.detail = ('Invalid user or password.')