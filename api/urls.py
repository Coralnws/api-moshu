from django.urls import path
from api.views.userApiView import *
from api.views.projectApiView import *
from api.views.documentApiView import *

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


    # Project
    path('project/<uuid:projectId>', ProjectDetailView.as_view(), name="project_detail"),
    path('project/create/<uuid:teamId>', ProjectCreateView.as_view(), name="create_project"),
    path('project/list', ProjectListView.as_view(), name="project_list"),
    

    # Document
    path('document/<uuid:documentId>', DocumentDetailView.as_view(), name="document_detail"),
    path('document/create/<uuid:projectId>', DocumentCreateView.as_view(), name="create_document"),
    path('document/list', DocumentListView.as_view(), name="document_list"),
    

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verfy'), 
]
    