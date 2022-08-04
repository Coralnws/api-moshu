import json
import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.documentSerializers import *
from ..models.documents import *
from ..models.deletions import *
from ..models.userRelations import UserProject, UserTeam
from ..api_throttles import *


""" For Admin(superuser)
GET: Get Document Detail By Id  # for any
PUT: Update Document By Id      # for superuser or owner
DELETE: Delete Document By Id (set isDelete = True)     # for superuser or owner
"""
class DocumentDetailView(generics.GenericAPIView):
    serializer_class = DocumentDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DocumentProfileSerializer
        return DocumentDetailSerializer

    # Get Document Detail By Id
    @swagger_auto_schema(operation_summary="Get Document Detail By Id")
    def get(self, request, documentId):
        # try:
            document = get_object_or_404(Document, pk=documentId,isDeleted=False)
            isMember = UserTeam.objects.filter(team=document.belongTo.belongTo, user =request.user).first()
            if isMember:
                serializer = self.get_serializer(instance=document)
                data = serializer.data
                data['message'] = "Get Document Detail Successfully"
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Not Team Member"}, status=status.HTTP_403_FORBIDDEN)
        # except:
        #     return Response({"message": "Get Document Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Document By Id
    @swagger_auto_schema(operation_summary="Update Document By Id")
    def put(self, request, documentId):
        # try:
            document = get_object_or_404(Document, pk=documentId,isDeleted=False)
            isMember = UserTeam.objects.filter(team=document.belongTo.belongTo, user =request.user).first()
            # if not request.user.is_staff and request.user != Document.createdBy:
            #     return Response({"message": "Unauthorized for Update Document"}, status=status.HTTP_401_UNAUTHORIZED)
            if isMember:
                data = request.data
                # data['content'].replace('\n', '\\n')
                # print("\n\njson parse\n", json.loads(data['content']),  "\ntype:", type(json.loads(data['content'])))
                serializer = self.get_serializer(instance=document, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Update Document Successfully"
                return Response(data, status=status.HTTP_200_OK)
            else :
                return Response({"message": "Unauthorized for Update Document"}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({"message": "Update Document Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Document By Id
    @swagger_auto_schema(operation_summary="Delete Document By Id")
    def delete(self, request, documentId):
        # try:
            document = get_object_or_404(Document, pk=documentId,isDeleted=False)
            isAdmin = UserTeam.objects.filter(team=document.belongTo.belongTo, user =request.user,isAdmin=True).first()
            if request.user == document.createdBy or request.user.is_staff or isAdmin:
                #document.delete()
            
                document.isDeleted=True
                document.save()
                deleteRecord = Deletion(deletedBy=request.user,type=1,belongTo=document.belongTo.belongTo)
                deleteRecord.save()
                document.deleteRecord=deleteRecord
                document.save()
                
                return Response({"message": "Delete Document Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Unauthorized for Delete Document"}, status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response({"message": "Delete Document Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Document
"""
class DocumentCreateView(generics.CreateAPIView):
    serializer_class = DocumentCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="Create Document")
    def post(self, request, projectId):
        # try:
            # isMember = UserProject.objects.get(project=projectId, user=request.user)
            project = get_object_or_404(Project, pk=projectId)
            isMember = UserTeam.objects.get(team=project.belongTo, user=request.user)
            if isMember:
                # if not isMember.isAdmin and not isMember.isMainAdmin:
                #     return Response({"message": "Unauthorized to Create Document in Project"}, status=status.HTTP_403_FORBIDDEN)
                project = get_object_or_404(Project, pk=projectId)
                data = request.data
                # data['content'].replace('\n', '\\n')
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(createdBy=request.user, belongTo=project)
                data = serializer.data
                data['message'] = "Create Document Successfully"
                return Response(data, status=status.HTTP_201_CREATED)
            else :
                return Response({"message": "Unauthorized to Create Document in Project"}, status=status.HTTP_403_FORBIDDEN)
        # except:
        #     return Response({"message": "Create Document Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Documents
"""
class DocumentListView(generics.ListAPIView):
    serializer_class = ListDocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Get All Documents
    @swagger_auto_schema(operation_summary="Get All Documents")
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
        allDocuments = Document.objects.filter(filter).order_by('-createdAt')
        return allDocuments; # will implement ordered By soon
