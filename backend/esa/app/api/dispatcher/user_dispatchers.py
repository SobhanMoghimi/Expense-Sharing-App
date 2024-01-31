from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from esa.app.api.controller.user_controller import UserController

urlpatterns = [
    path('info/', UserController.as_view({'get':'get_user_info'})),
    path('login/', UserController.as_view({'post': 'login'}), name='login'),
    path('logout/', UserController.as_view({'post': 'logout'}), name='logout'),
    path('register/', UserController.as_view({'post': 'register'})),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
