from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from esa.app.api.serializer.customer.customer_serializers import CustomerLoginRequestSerializer, TokenSerializer, \
    RefreshTokenSerializer
from esa.app.api.serializer.system.system_serializer import ResponseSerializer
from esa.app.helpers.common_response import ErrorResponse, SuccessfulResponse
from esa.app.helpers.exceptions.exceptions import UserNotFoundException
from esa.app.helpers.utils.esa_utils import ESAUtils
from esa.app.logic.mmb_logic import MarketMakerLogic
from esa.app.models.dtos.dtos import TokenDTO, LoginDTO, LogoutDto


class AuthController(viewsets.ViewSet):
    permission_classes_by_action = {'login': [AllowAny]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def __init__(self):
        super().__init__()
        self.logic = MarketMakerLogic()

    @extend_schema(
        request=CustomerLoginRequestSerializer,
        tags=['Authentication'],
        summary='request to login',
        description="",
        responses=TokenSerializer,
    )
    def login(self, request: Request):
        try:
            validated_data = LoginDTO(**request.data)
            result = self.logic.login(validated_data)
            response = TokenDTO(**result)
            return Response(response.model_dump(), status=status.HTTP_201_CREATED)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except UserNotFoundException as e:
            return ErrorResponse(message=e, status_code=e.status_code)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @extend_schema(
        request=RefreshTokenSerializer,
        tags=["Authentication"],
        summary='log out user',
        description='it will revoke refresh token and log out user from panel',
        responses={200: ResponseSerializer},
    )
    def logout(self, request: Request):
        try:
            validated_data = LogoutDto(**request.data)
            self.logic.logout(validated_data)
            return SuccessfulResponse()
        except (ValueError, TokenError) as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

