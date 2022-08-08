from django.urls import path
from api.views.userApiView import *
from api.views.teamApiView import *
from api.views.projectApiView import *
from api.views.documentApiView import *
from api.views.diagramApiView import *
from api.views.recycleApiVew import *


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
    path('team/invite', InviteView.as_view(), name="team_invite"), 
    path('team/leave/<uuid:teamId>', LeaveTeamView.as_view(), name="team_leave"),
    path('team/member/remove/<uuid:teamId>/<uuid:userId>', RemoveMemberView.as_view(), name="remove_team_member"),
    path('team/member/list/<uuid:teamId>', TeamMemberView.as_view(), name="list_team_member"),
    path('team/admin/set/<uuid:teamId>/<uuid:userId>', SetAdminView.as_view(), name="set_team_admin"),
    path('team/admin/remove/<uuid:teamId>/<uuid:userId>', RemoveAdminView.as_view(), name="remove_team_admin"),
    path('invitation/reply/<uuid:invitationId>/<int:result>', ReplyTeamInvitationView.as_view(), name="reply_invitation"),
    path('invitation/list', ListInvitationView.as_view(), name="list_invitations"),
    
    #token

    # Project
    path('project/<uuid:projectId>', ProjectDetailView.as_view(), name="project_detail"),
    path('project/create/<uuid:teamId>', ProjectCreateView.as_view(), name="create_project"),
    path('project/list', ProjectListView.as_view(), name="project_list"),

    path('image/', UploadImageView.as_view(), name="upload_image"),
    
    #Diagram
    path('diagram/create/<uuid:projectId>', DiagramCreateView.as_view(), name="diagram_create"),
    path('diagram/<uuid:diagramId>', DiagramDetailView.as_view(), name="diagram_detail"),
    path('diagram/list', DiagramListView.as_view(), name="diagram_list"),

    # Document
    path('document/<uuid:documentId>', DocumentDetailView.as_view(), name="document_detail"),
    path('document/<uuid:documentId>/changes', DocumentChangesView.as_view(), name="document_changes"),
    path('document/create/<uuid:projectId>', DocumentCreateView.as_view(), name="create_document"),
    path('document/list', DocumentListView.as_view(), name="document_list"),
    
    #Recovery
    #path('recovery/project/<uuid:deleteRecordId>', RecoverProjectView.as_view(), name="recover_project"),
    #path('recovery/document/<uuid:deleteRecordId>', RecoverDocumentView.as_view(), name="recover_document"),
    #path('recovery/diagram/<uuid:deleteRecordId>', RecoverDiagramView.as_view(), name="recover_diagram"),

    path('recovery/<uuid:deleteRecordId>', RecoveryView.as_view(), name="recover_project"),
    path('recovery/list/<uuid:teamId>', RecoveryListView.as_view(), name="recovery_list"),
    path('recovery/clear/<uuid:teamId>', ClearAllView.as_view(), name="clear_recycleBin"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verfy'), 
]
    
