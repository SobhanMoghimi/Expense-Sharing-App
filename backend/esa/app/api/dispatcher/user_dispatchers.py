from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from esa.app.api.controller.user_controller import AuthController

urlpatterns = [
    path('login/', AuthController.as_view({'post': 'login'}), name='login'),
    path('logout/', AuthController.as_view({'post': 'logout'}), name='logout'),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
