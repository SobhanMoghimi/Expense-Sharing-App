from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from esa.app.api.controller.user_controller import UserController, GroupController

urlpatterns = [
    path('', GroupController.as_view({'post':'create_group', 'get':'get_user_groups'})),
]