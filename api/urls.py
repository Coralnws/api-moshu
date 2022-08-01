from django.urls import path
from api.views.userApiView import *

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    # User Authentication 
    path('auth/register/', UserRegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verfy'), 
]
    