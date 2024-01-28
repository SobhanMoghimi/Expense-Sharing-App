from typing import Any

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'
    default_code = 'not_found'

class AlreadyExistsException(APIException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, detail: str = None):
        super().__init__(detail=detail)


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


class UserWithPasswordNotFoundException(NotFound):
    def __init__(self):
        super().__init__()
        self.detail = ('Invalid user or password.')

class UserNotFoundException(NotFound):
    def __init__(self):
        super().__init__()
        self.detail = ('User not found!')

class InvalidPhoneNumberException(ValidationError):
    def __init__(self):
        super().__init__(detail=['phone number is not valid'], code=status.HTTP_400_BAD_REQUEST)
