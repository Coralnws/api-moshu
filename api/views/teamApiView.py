import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.teamSerializers import *
from ..serializers.userSerializers import *
from ..serializers.invitationSerializers import *
from ..utils import *
from ..models.teams import Team
from ..models.userRelations import *
from ..models.invitations import Invitation

"""
GET : Get a team by Id
PUT: Update Team By Id 
DELETE: Delete Team By Id
"""
class TeamDetailView(generics.GenericAPIView):
    serializer_class = TeamDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TeamProfileSerializer #showing info
        return TeamDetailSerializer  #when update or delete

    # Get Team Detail By Id
    @swagger_auto_schema(operation_summary="Get Team Detail By Id")
    def get(self, request, teamId):
        # try:
            team = get_object_or_404(Team, pk=teamId)
            members = UserTeam.objects.filter(team=teamId).count()
            team.members = members
            serializer = self.get_serializer(instance=team)
            data = serializer.data
            data['message'] = "Get Team Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)

        # except:
        #     return Response({"message": "Get Team Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Team By Id
    @swagger_auto_schema(operation_summary="Update Team By Id")
    def put(self, request, teamId):
        admin = UserTeam.objects.filter(team=teamId, user=request.user, isAdmin=True)

        if admin:
            team = get_object_or_404(Team, pk=teamId)
            serializer = self.get_serializer(instance=team, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update Team Successfully"
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Update Team Failed,Not Team Admin"}, status=status.HTTP_400_BAD_REQUEST)

    # Delete Team By Id
    @swagger_auto_schema(operation_summary="Delete Team By Id")
    def delete(self, request, teamId):
        isMainAdmin = UserTeam.objects.filter(team=teamId, user=request.user, isMainAdmin=True).first()
        if isMainAdmin:
            try:
                team = get_object_or_404(Team, pk=teamId)
                team.delete()
                return Response({"message": "Delete Team Successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Delete Team Failed,Not Team Creator"}, status=status.HTTP_400_BAD_REQUEST)

'''
POST:Create Team
'''
class TeamCreateView(generics.CreateAPIView):
    serializer_class = TeamCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Create Team")
    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user)

        #add new UserTeam
        team = get_object_or_404(Team, pk=serializer.data["id"])
        newUserTeam = UserTeam(team=team, user=request.user,isAdmin=True,isMainAdmin=True)
        newUserTeam.save()
        data = serializer.data
        data['message'] = "Create Team Successfully"
        return Response(data, status=status.HTTP_201_CREATED)

"""
POST:Invite
"""
class InviteView(generics.GenericAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Invite,user:target")
    def post(self,request):  #userId is user who wish to invite
        try:
            team = get_object_or_404(Team, pk=request.data['team'])
            isAdmin = UserTeam.objects.filter(team=team, user=request.user,isAdmin=True)
            isMember = UserTeam.objects.filter(team=team, user=request.data['user'])
            userInvite = get_object_or_404(CustomUser, pk=request.data['user'])
            if not isAdmin:
                return Response({"message": "You are not admin of this team."}, status=status.HTTP_403_FORBIDDEN)
            
            if isMember:
                return Response({"message": "User is team member."}, status=status.HTTP_403_FORBIDDEN)


            record = Invitation.objects.filter(team=team, user=userInvite).first()
            data = {'user':userInvite.id,'team':team.id,'invitedBy':request.user.id,'result':0}
            if record:
                serializer = self.get_serializer(instance=record,data=data)
            else:
                serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            data['message'] = "Invitation Sent."
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Failed to invite."}, status=status.HTTP_400_BAD_REQUEST)

"""
POST:Reply Invitation
"""
class ReplyTeamInvitationView(generics.GenericAPIView):
    serializer_class = ReplyInvitationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Reply invitation,result: 1-accept,2-decline")
    def put(self,request,invitationId,result):
        #try:
            invitation = get_object_or_404(Invitation, pk=invitationId)
            
            #if invitation.user == request.user and not invitation.result:
            if not invitation.result:
                if result == 1:
                    invitation.result = result
                    invitation.save()
                    newUserTeam = UserTeam(team=invitation.team, user=invitation.user)
                    newUserTeam.save()
                    return Response({"message": "Accept Invitation,Join Team Successfully."}, status=status.HTTP_201_CREATED)
                if result == 2:
                    invitation.result = result
                    invitation.save()
                    return Response({"message": "Refuse Invitation Successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Invitation was replied/Not User."}, status=status.HTTP_200_OK)
            
        #except:
           # return Response({"message": "Reply Invitation Failed"}, status=status.HTTP_400_BAD_REQUEST)



"""
Leave Team
"""
class LeaveTeamView(generics.GenericAPIView):
    serializer_class = UserTeamJoinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Leave Team")
    def delete(self, request, teamId):
        isMember = UserTeam.objects.get(team=teamId, user=request.user)
        if isMember:
            if not isMember.isMainAdmin:
                isMember.delete()
                return Response({"message": "Leave Team Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Leave Team Failed, You Are Main Admin Of The Team"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Leave Team Failed, Not Team Member"}, status=status.HTTP_401_UNAUTHORIZED)



###################### Team Admin #############################
"""
Remove team member
"""
class RemoveMemberView(generics.GenericAPIView):
    serializer_class = UserTeamJoinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]   

    @swagger_auto_schema(operation_summary="Remove Team Member,userId:target")
    def delete(self, request, teamId,userId): #userId: member to remove
        isAdmin = UserTeam.objects.filter(team=teamId, user=request.user, isAdmin=True).first()
        if isAdmin:
            try:
                userTeam = get_object_or_404(UserTeam, team=teamId,user=userId)
                userTeam.delete()
                return Response({"message": "Remove Member Successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Remove member failed,he/she is not team member."}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"message": "Remove member failed,you are not team admin."}, status=status.HTTP_400_BAD_REQUEST) 

"""
PUT:Set Admin
"""
class SetAdminView(generics.GenericAPIView):
    serializer_class = UserTeamDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Set Team Admin Role,userId=target")
    def put(self,request,teamId,userId):
        userAdmin = UserTeam.objects.filter(team=teamId, user=request.user,isAdmin=True)

        if userAdmin:
            userTarget = get_object_or_404(UserTeam, team=teamId, user=userId)
            serializer = self.serializer_class(instance=userTarget,data={'isAdmin':True})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            #data = serializer.data
            #data['message'] = "Set Admin Successfully"
            return Response({"message": "Set Admin Successfully"}, status=status.HTTP_200_OK)
            
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)


"""
PUT:Remove Admin
"""
class RemoveAdminView(generics.GenericAPIView):
    serializer_class = UserTeamDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Remove Team Admin Role,userId=target")
    def put(self,request,teamId,userId):
        userAdmin = UserTeam.objects.filter(team=teamId, user=request.user,isMainAdmin=True)

        if userAdmin:
            userTarget = get_object_or_404(UserTeam, team=teamId, user=userId)
            serializer = self.serializer_class(instance=userTarget,data={'isAdmin':False})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            #data = serializer.data
            #data['message'] = "Remove Admin Successfully"
            return Response({"Remove Admin Successfully"}, status=status.HTTP_200_OK)
            
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)



########################## List ####################################
## Inside
"""
GET:Show all member
"""
class TeamMemberView(generics.ListAPIView):
    serializer_class = ListMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get All Team Member,?type=main/admin/normal")
    def get_queryset(self):
        team = self.kwargs['teamId']
        type = self.request.GET.get('type')  #main/admin/normal
        isMember = UserTeam.objects.get(team=team, user=self.request.user)
        if isMember is None:
            return Response({"message": "Not Team Member"}, status=status.HTTP_403_FORBIDDEN)

        filter = Q()
        filter &= Q(userteam__team=team)

        if type is not None:
            if type == 'main':
                filter &= Q(userteam__isMainAdmin=True)
            elif type == 'admin':
                filter &= Q(userteam__isAdmin=True)
            elif type == 'normal':
                filter &= Q(userteam__isAdmin=False,userteam_isMainAdmin=False)

                
        allMember = CustomUser.objects.filter(filter)
        for member in allMember:
            admin = UserTeam.objects.filter(user=member, team=team).first()
            if admin.isMainAdmin:
                member.position = '0'
            elif admin.isAdmin:
                member.position = '1'
            else:
                member.position = '2'
        ordered = sorted(allMember, key=operator.attrgetter('position'))
        return ordered


## Outside
"""
GET: Show All Team join by user + user's position + member
"""
class ShowUserTeamView(generics.ListAPIView):
    serializer_class = ListTeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get All Team Joined by User")
    def get_queryset(self):
        allTeams = Team.objects.filter(userteam__user=self.request.user)
        for team in allTeams:
            members = UserTeam.objects.filter(team=team).count()
            userTeam = get_object_or_404(UserTeam, team=team, user=self.request.user)
            team.members = members
            team.joinedAt = userTeam.createdAt
            if userTeam.isMainAdmin:
                #team.position="MainAdmin/Creator"
                team.position='M'
            elif userTeam.isAdmin:
                #team.position="Admin"
                team.position='A'
            else:
                #team.position="Normal"
                team.position='N'
        ordered = sorted(allTeams, key=operator.attrgetter('joinedAt'), reverse=False)
        return ordered


"""
List Invitation
"""
class ListInvitationView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get All Pending Invitation")
    def get_queryset(self):
        allInvitations = Invitation.objects.filter(user=self.request.user,result=0)
        ordered = sorted(allInvitations, key=operator.attrgetter('createdAt'), reverse=False)
        return ordered


