from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from esa.app.api.controller.user_controller import UserController

urlpatterns = [
    path('login/', UserController.as_view({'post': 'login'}), name='login'),
    path('logout/', UserController.as_view({'post': 'logout'}), name='logout'),
    path('register/', UserController.as_view({'post': 'register'})),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friends/', UserController.as_view({'post': 'add_friend', "get": 'get_friends'})),
]
