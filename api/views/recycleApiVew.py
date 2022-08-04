import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.recoverySerializers import *
from ..models.projects import *
from ..models.documents import *
from ..models.diagrams import *
from ..models.deletions import *
from ..models.userRelations import UserTeam
from ..api_throttles import *


class RecoverProjectView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Project")
    def put(self, request, deleteRecordId):
        project = get_object_or_404(Project, deleteRecord=deleteRecordId)
        project.isDeleted=False
        project.save()
        allDocuments = Document.objects.filter(belongTo=project)
        for document in allDocuments:
            document.isDeleted=False
            #document.deleteRecord = null
        allDiagrams = Diagram.objects.filter(belongTo=project)
        for diagram in allDiagrams:
            diagram.isDeleted=False
            #diagram.deleteRecord = null
        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Recover Project Successfully"}, status=status.HTTP_200_OK)

    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Project By Id")
    def delete(self, request, deleteRecordId):
        project = get_object_or_404(Project, deleteRecord=deleteRecordId)
        project.delete()
        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Delete Project Successfully"}, status=status.HTTP_200_OK)


class RecoverDocumentView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Document")
    def put(self, request, deleteRecordId):
        document = get_object_or_404(Document, deleteRecord=deleteRecordId)
        document.isDeleted=False
        document.save()
        #document.deleteRecord = null

        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Recover Document Successfully"}, status=status.HTTP_200_OK)

    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Document By Id")
    def delete(self, request, deleteRecordId):
        document = get_object_or_404(Document, deleteRecord=deleteRecordId)
        document.delete()
        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Delete Document Successfully"}, status=status.HTTP_200_OK)

class RecoverDiagramView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Diagram")
    def put(self, request, deleteRecordId):
        diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
        diagram.isDeleted=False
        diagram.save()
        #diagram.deleteRecord = null

        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Recover Diagram Successfully"}, status=status.HTTP_200_OK)

    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Diagram By Id")
    def delete(self, request, deleteRecordId):
        diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
        diagram.delete()
        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Delete Diagram Successfully"}, status=status.HTTP_200_OK)


class RecoveryListView(generics.ListAPIView):
    serializer_class = ListRecoverySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Get All Projects
    @swagger_auto_schema(operation_summary="List all Recycle bin")
    def get_queryset(self):
        team = self.kwargs['teamId']
        
        allRecovery = Deletion.objects.filter(belongTo=team).order_by('-createdAt')
        return allRecovery