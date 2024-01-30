from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from esa.app.api.serializer.user.user_serializers import CustomerLoginRequestSerializer, TokenSerializer, \
    RefreshTokenSerializer, UserRegisterRequestSerializer, CreateGroupRequestSerializer, GroupSerializer, \
    GroupListSerializer, AddGroupMemberRequestSerializer, AddFriendRequestSerializer, FriendsSerializer, \
    AddFriendExpenseRequestSerializer, GetFriendExpensesRequestSerializer
from esa.app.api.serializer.system.system_serializer import ResponseSerializer
from esa.app.helpers.common_response import ErrorResponse, SuccessfulResponse
from esa.app.helpers.exceptions.exceptions import UserWithPasswordNotFoundException
from esa.app.helpers.utils.esa_utils import ESAUtils
from esa.app.logic.esa_logic import ExpenseSharingAPPLogic
from esa.app.models.dtos.dtos import TokenDTO, LoginDTO, LogoutDto, FriendExpenseDTO


class UserController(viewsets.ViewSet):
    permission_classes_by_action = {'login': [AllowAny], 'register': [AllowAny]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def __init__(self):
        super().__init__()
        self.logic = ExpenseSharingAPPLogic()


    @extend_schema(
        request=UserRegisterRequestSerializer,
        tags=["Authentication"],
        responses={201: TokenSerializer},
    )
    def register(self, request: Request):
        serializer = UserRegisterRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                password = serializer.validated_data.get("password")
                first_name = serializer.validated_data.get("first_name")
                last_name = serializer.validated_data.get("last_name")
                email = serializer.validated_data.get("email")
                phone_number = serializer.validated_data.get("phone_number")
                response = self.logic.register(first_name, last_name, email, phone_number, password)
                return Response(response.model_dump(), status=status.HTTP_201_CREATED)
            else:
                return ErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)
        except APIException as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e.detail, status_code=e.status_code)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

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
        except UserWithPasswordNotFoundException as e:
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

class FriendsController(viewsets.ViewSet):
    def __init__(self):
        super().__init__()
        self.logic = ExpenseSharingAPPLogic()

    @extend_schema(
        request=AddFriendRequestSerializer,
        tags=['Friends'],
        summary='Add Friend',
        description="",
        responses={200: ResponseSerializer},
    )
    def add_friend(self, request: Request):
        serializer = AddFriendRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = request.user
                phone_or_email = serializer.validated_data.get("phone_number_or_email")
                self.logic.add_friend(user, phone_or_email)
                # response_serializer = GroupSerializer(response)
                # return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return SuccessfulResponse()
            else:
                return ErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @extend_schema(
        tags=['Friends'],
        summary='Get Friends',
        description="",
        responses={200: FriendsSerializer},
    )
    def get_friends(self, request: Request):
        try:
            user = request.user
            response = self.logic.get_friends(user)
            response_serializer = FriendsSerializer({'friends': response})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @extend_schema(
        request=AddFriendExpenseRequestSerializer,
        tags=['Friends'],
        summary='Add Friend Expense',
        description="",
        responses={200: ResponseSerializer},
    )
    def add_expense(self, request: Request):
        serializer = AddFriendExpenseRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = request.user
                expense_dto = FriendExpenseDTO.model_validate(serializer.data)
                expense_dto.created_by = user
                self.logic.add_friend_expense(
                    expense_dto
                )
                return SuccessfulResponse()
            else:
                return ErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @extend_schema(
        request=GetFriendExpensesRequestSerializer,
        tags=['Friends'],
        summary='Get Friends Expense',
        description="",
        responses={200: FriendsSerializer},
    )
    def get_friends_expenses(self, request: Request):
        serializer = GetFriendExpensesRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = request.user
                friend_id = serializer.validated_data.get("friend_id")
                output = self.logic.get_friends_expenses(
                    user,
                    friend_id
                )
                return SuccessfulResponse()
            else:
                return ErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


class GroupController(viewsets.ViewSet):
    permission_classes_by_action = {'login': [AllowAny], 'register': [AllowAny]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def __init__(self):
        super().__init__()
        self.logic = ExpenseSharingAPPLogic()

    @extend_schema(
        request=CreateGroupRequestSerializer,
        tags=['Group'],
        summary='Create Group',
        description="",
        responses=GroupSerializer,
    )
    def create_group(self, request: Request):
        serializer = CreateGroupRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = request.user
                group_name = serializer.validated_data.get("name")
                group_description = serializer.validated_data.get("description")
                response = self.logic.create_group(user, group_name, group_description)
                response_serializer = GroupSerializer(response)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return ErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @extend_schema(
        request=AddGroupMemberRequestSerializer,
        tags=['Group'],
        summary='Add Group Member',
        description="",
        responses=GroupSerializer,
    )
    def add_group_member(self, request: Request):
        serializer = AddGroupMemberRequestSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = request.user
                group_id = serializer.validated_data.get("group_id")
                user_id = serializer.validated_data.get("user_id")
                response = self.logic.add_group_member(user, group_id, user_id)
                response_serializer = GroupSerializer(response)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return ErrorResponse(status_code=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


    @extend_schema(
        tags=['Group'],
        summary='Get user groups',
        description="",
        responses=GroupListSerializer,
    )
    def get_user_groups(self, request: Request):
        try:
            user = request.user
            groups = self.logic.get_user_groups(user)
            response_serializer = GroupListSerializer({'groups': groups})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ESAUtils.handle_exception(e)
            return ErrorResponse(message=e, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
