from datetime import datetime

from _decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StrictInt, Field, StrictStr, condecimal, field_validator, PastDatetime, \
    FutureDatetime

from esa.app.models import UserEntity
from esa.app.models.enums import RequestMethod, SplitType


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_default=True,
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )
    created_at: datetime | None = None


class LoginDTO(BaseModel):
    email: str = Field(title='user\'s email',
                       description='this field is user\'s email what registered in Invex')
    password: str = Field(title='user\'s password',
                          description='this field is user\'s password what registered in Invex')


class TokenDTO(BaseModel):
    access_token: str = Field(title='user\'s access token',
                              description='this token expires after 15 minutes')
    refresh_token: str = Field(title='user\'s refresh token',
                               description='this token expires after 60 days')


class LogoutDto(BaseDTO):
    refresh_token: str

    @field_validator('refresh_token')
    def _check_refresh_token_in_not_null(cls, refresh_token):
        if not bool(refresh_token):
            raise ValueError('refresh_token can not be None')
        return refresh_token


class RequestDTO(BaseDTO):
    method: RequestMethod
    url: str
    max_retry: int = 5
    backoff_factor: int = 1
    headers: dict | None = None
    params: dict | None = None
    data: dict | None = None

class FriendExpenseDTO(BaseDTO):
    created_by: UUID | UserEntity | None = None
    title: StrictStr
    description: StrictStr | None = None
    amount: StrictInt
    paid_by: UUID | UserEntity
    other_user: UUID | UserEntity
    split_type: SplitType
    payer_amount: StrictInt | None = None
    other_amount: StrictInt | None = None
    payer_percentage: StrictInt | None = None
    other_percentage: StrictInt | None = None
