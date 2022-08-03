from django.urls import path
from api.views.userApiView import *
from api.views.teamApiView import *

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

    #Team Management
    path('team/list', ShowUserTeamView.as_view(), name="list_team"),
    path('team/create', TeamCreateView.as_view(), name="create_team"),
    path('team/<uuid:teamId>', TeamDetailView.as_view(), name="team_detail"),
    path('team/invite/<uuid:teamId>/<uuid:userId>', InviteView.as_view(), name="team_invite"), 
    path('team/leave/<uuid:teamId>', LeaveTeamView.as_view(), name="team_leave"),
    path('team/member/remove/<uuid:teamId>/<uuid:userId>', RemoveMemberView.as_view(), name="remove_team_member"),
    path('team/member/list/<uuid:teamId>', TeamMemberView.as_view(), name="list_team_member"),
    path('team/admin/set/<uuid:teamId>/<uuid:userId>', SetAdminView.as_view(), name="set_team_admin"),
    path('team/admin/remove/<uuid:teamId>/<uuid:userId>', RemoveAdminView.as_view(), name="remove_team_admin"),
    path('invitation/reply/<uuid:invitationId>/result', InviteView.as_view(), name="reply_invitation"),
    path('invitation/list', ListInvitationView.as_view(), name="list_invitations"),
    
    #token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verfy'), 
]
    