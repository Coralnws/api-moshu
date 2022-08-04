import json
import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.diagramSerializers import *
from ..models.diagrams import *
from ..models.projects import *
from ..models.userRelations import UserProject, UserTeam
from ..api_throttles import *


""" For Admin(superuser)
GET: Get Diagram Detail By Id  # for any
PUT: Update Diagram By Id      # for superuser or owner
DELETE: Delete Diagram By Id (set isDelete = True)     # for superuser or owner
"""
class DiagramDetailView(generics.GenericAPIView):
    serializer_class = DiagramDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DiagramProfileSerializer
        return DiagramDetailSerializer

    # Get Diagram Detail By Id
    @swagger_auto_schema(operation_summary="Get Diagram Detail By Id")
    def get(self, request, diagramId):
        # try:
            diagram = get_object_or_404(Diagram, pk=diagramId,isDeleted=False)
            
            serializer = self.get_serializer(instance=diagram)
            data = serializer.data
            data['message'] = "Get Diagram Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        # except:
        #     return Response({"message": "Get Diagram Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Diagram By Id
    @swagger_auto_schema(operation_summary="Update Diagram By Id")
    def put(self, request, diagramId):
        # try:
            diagram = get_object_or_404(Diagram, pk=diagramId,isDeleted=False)
            isMember = UserTeam.objects.filter(team=diagram.belongTo.belongTo, user =request.user).first()
            
            if isMember:
                data = request.data
                # data['content'].replace('\n', '\\n')
                # print("\n\njson parse\n", json.loads(data['content']),  "\ntype:", type(json.loads(data['content'])))
                serializer = self.get_serializer(instance=Diagram, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Update Diagram Successfully"
                return Response(data, status=status.HTTP_200_OK)
            else :
                return Response({"message": "Unauthorized for Update Diagram"}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({"message": "Update Diagram Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Diagram By Id
    @swagger_auto_schema(operation_summary="Delete Diagram By Id")
    def delete(self, request, diagramId):
        # try:
            diagram = get_object_or_404(diagram, pk=diagramId,isDeleted=False)
            isAdmin = UserTeam.objects.filter(team=diagram.belongTo.belongTo, user =request.user,isAdmin=True).first()
            if request.user == diagram.createdBy or request.user.is_staff or isAdmin:
                diagram.delete()

                '''
                diagram.isDeleted=True
                diagram.save()
                deleteRecord = Deletion(deletedBy=request.user,type=1,belongTo=diagram.belongTo.belongTo)
                deleteRecord.save()
                diagram.deleteRecord=deleteRecord
                '''
                return Response({"message": "Delete Diagram Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Unauthorized for Delete Diagram"}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({"message": "Delete Diagram Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Diagram
"""
class DiagramCreateView(generics.CreateAPIView):
    serializer_class = DiagramCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="Create Diagram")
    def post(self, request, projectId):
        # try:
            # isMember = UserProject.objects.get(project=projectId, user=request.user)
            project = get_object_or_404(Project, pk=projectId)
            #isMember = UserTeam.objects.get(team=project.belongTo, user=request.user)
            #if isMember:
                # if not isMember.isAdmin and not isMember.isMainAdmin:
                #     return Response({"message": "Unauthorized to Create Diagram in Project"}, status=status.HTTP_403_FORBIDDEN)
            project = get_object_or_404(Project, pk=projectId)
            print(type(request.data['content']))
            data = request.data
            # data['content'].replace('\n', '\\n')
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(createdBy=request.user, belongTo=project)
            data = serializer.data
            data['content'] = { 'children': data['content']}
            print(type(data['content']))
            data['message'] = "Create Diagram Successfully"
            return Response(data, status=status.HTTP_201_CREATED)   
            #else :
             #   return Response({"message": "Unauthorized to Create Diagram in Project"}, status=status.HTTP_403_FORBIDDEN)
        # except:
        #     return Response({"message": "Create Diagram Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Diagrams
"""
class DiagramListView(generics.ListAPIView):
    serializer_class = ListDiagramSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Get All Diagrams
    @swagger_auto_schema(operation_summary="Get All Diagrams")
    def get_queryset(self):
        search = self.request.GET.get('search')
        project = self.request.GET.get('belongTo')
        createdBy = self.request.GET.get('createdBy')

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(content__icontains=term) | Q(description__icontains=term) | Q(createdBy__username__icontains=term)

        if project is not None:
            filter &= Q(belongTo=project)

        if createdBy is not None:
            filter &= Q(createdBy = createdBy)

        filter &= Q(isDeleted=False)
        allDiagrams = Diagram.objects.filter(filter).order_by('-createdAt')
        return allDiagrams; # will implement ordered By soon



class UploadImageView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="Upload Image")
    def post(self, request):
        # try:
            # isMember = UserProject.objects.get(project=projectId, user=request.user)
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        
        # except:
        #     return Response({"message": "Create Diagram Failed"}, status=status.HTTP_400_BAD_REQUEST)
