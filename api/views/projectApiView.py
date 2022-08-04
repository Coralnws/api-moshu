import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.projectSerializers import *
from ..models.projects import *
from ..models.userRelations import UserTeam
from ..api_throttles import *


""" For Admin(superuser)
GET: Get Project Detail By Id  # for any
PUT: Update Project By Id      # for superuser or owner
DELETE: Delete Project By Id (set isDelete = True)     # for superuser or owner
"""
class ProjectDetailView(generics.GenericAPIView):
    serializer_class = ProjectDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProjectProfileSerializer
        return ProjectDetailSerializer

    # Get Project Detail By Id
    @swagger_auto_schema(operation_summary="Get Project Detail By Id")
    def get(self, request, projectId):
        # try:
            project = get_object_or_404(Project, pk=projectId)
            
            serializer = self.get_serializer(instance=project)
            data = serializer.data
            data['message'] = "Get Project Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        # except:
        #     return Response({"message": "Get Project Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Update Project By Id")
    def put(self, request, projectId):
        # try:
            project = get_object_or_404(Project, pk=projectId)
            isMember = UserTeam.objects.filter(team=project.belongTo.id, user=request.user).first()
            # will open permission for when the person is the mainAdmin or admin of the team
            # if not request.user.is_staff and request.user != project.createdBy:
            #     return Response({"message": "Unauthorized for update feed"}, status=status.HTTP_401_UNAUTHORIZED)
            if isMember:
                serializer = self.get_serializer(instance=project, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Update Project Successfully"
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Unauthorized for update Project"}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({"message": "Update Project Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Project By Id")
    def delete(self, request, projectId):
        # try:
            project = get_object_or_404(Project, pk=projectId)
            isMember = UserTeam.objects.filter(team=project.belongTo.id, user=request.user).first()
            if isMember:
                project.delete()
                return Response({"message": "Delete Project Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Unauthorized for Delete Project"}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({"message": "Delete Project Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Project
"""
class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="Create Project")
    def post(self, request, teamId):
        # try:
            isMember = UserTeam.objects.filter(team=teamId, user=request.user).first()
            # print("isMember", isMember)
            if isMember:
                # if not isMember.isAdmin and not isMember.isMainAdmin:
                #     return Response({"message": "Unauthorized to Create Project in Team"}, status=status.HTTP_403_FORBIDDEN)
                team = get_object_or_404(Team, pk=teamId)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(createdBy=request.user, belongTo=team)
                data = serializer.data
                data['message'] = "Create Project Successfully"
                return Response(data, status=status.HTTP_201_CREATED)
            else :
                return Response({"message": "Unauthorized to Create Project in Team"}, status=status.HTTP_403_FORBIDDEN)
        # except:
        #     return Response({"message": "Create Project Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Projects
"""
class ProjectListView(generics.ListAPIView):
    serializer_class = ListProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Get All Projects
    @swagger_auto_schema(operation_summary="Get All Projects")
    def get_queryset(self):
        search = self.request.GET.get('search')
        team = self.request.GET.get('belongTo')
        createdBy = self.request.GET.get('createdBy')

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(description__icontains=term) | Q(createdBy__username__icontains=term)

        if team is not None:
            filter &= Q(belongTo=team)

        if createdBy is not None:
            filter &= Q(createdBy = createdBy)

        allProjects = Project.objects.filter(filter).order_by('-createdAt')
        return allProjects; # will implement ordered By soon
