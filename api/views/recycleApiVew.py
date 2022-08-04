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

'''
class RecoverProjectView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Project")
    def put(self, request, deleteRecordId):
        project = get_object_or_404(Project, deleteRecord=deleteRecordId)
        project.isDeleted=False
        allDocuments = Document.objects.filter(belongTo=project)
        for document in allDocuments:
            document.isDeleted=False
            document.deleteRecord = null
        allDiagrams = Diagram.objects.filter(belongTo=project)
        for diagram in allDiagrams:
            diagram.isDeleted=False
            diagram.deleteRecord = null
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
    @swagger_auto_schema(operation_summary="Recover Project")
    def put(self, request, deleteRecordId):
        document = get_object_or_404(Document, deleteRecord=deleteRecordId)
        document.isDeleted=False
        document.deleteRecord = null

        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Recover Project Successfully"}, status=status.HTTP_200_OK)

    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Project By Id")
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
    @swagger_auto_schema(operation_summary="Recover Project")
    def put(self, request, deleteRecordId):
        diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
        diagram.isDeleted=False
        diagram.deleteRecord = null

        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Recover Project Successfully"}, status=status.HTTP_200_OK)

    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Project By Id")
    def delete(self, request, deleteRecordId):
        diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
        diagram.delete()
        deleteRecord = Deletion.objects.get(pk=deleteRecordId)
        deleteRecord.delete()
        return Response({"message": "Delete Diagram Successfully"}, status=status.HTTP_200_OK)

'''