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


class RecoveryView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recovery,just fill in deleteRecordId")
    def put(self, request, deleteRecordId):
        record = get_object_or_404(Deletion,pk=deleteRecordId)
        isMember = UserTeam.objects.filter(team=record.belongTo, user=request.user).first() 
        if isMember:
            if record.type == 0:
                project = get_object_or_404(Project, deleteRecord=deleteRecordId)
                project.isDeleted=False
                project.save()
                allDocuments = Document.objects.filter(belongTo=project)
                for document in allDocuments:
                    document.isDeleted=False
                    document.save()
                    #document.deleteRecord = null
                allDiagrams = Diagram.objects.filter(belongTo=project)
                for diagram in allDiagrams:
                    diagram.isDeleted=False
                    diagram.save()
                    #diagram.deleteRecord = null
            elif record.type == 1:
                document = get_object_or_404(Document, deleteRecord=deleteRecordId)
                document.isDeleted=False
                document.save()
            
            elif record.type == 2:
                diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
                diagram.isDeleted=False
                diagram.save()
            record.delete()
            return Response({"message": "Recover Project Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)


    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Project By Id")
    def delete(self, request, deleteRecordId):
        record = get_object_or_404(Deletion,pk=deleteRecordId)
        isMember = UserTeam.objects.filter(team=record.belongTo, user=request.user).first() 
        if isMember:
            if record.type == 0:
                project = get_object_or_404(Project, deleteRecord=deleteRecordId)
                project.delete()
                
            elif record.type == 1:
                document = get_object_or_404(Document, deleteRecord=deleteRecordId)
                document.delete()
            
            elif record.type == 2:
                diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
                diagram.delete()
            record.delete()
            return Response({"message": "Delete Project Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)


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

class ClearAllView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]
    
    @swagger_auto_schema(operation_summary="Empty Recycle Bin")
    def delete(self, request, teamId):
        allRecord = Deletion.objects.filter(belongTo=teamId)
        isMember = UserTeam.objects.filter(team=teamId, user =request.user).first() 
        if isMember:
            for record in allRecord:
                if record.type == 0: #project
                    project = get_object_or_404(Project, deleteRecord=record)
                    project.delete()
                
                elif record.type == 1: #document
                    document = get_object_or_404(Document, deleteRecord=record)
                    document.delete()
                
                elif record.type == 2: #diagram
                    diagram = get_object_or_404(Diagram, deleteRecord=record)
                    diagram.delete()
                
                record.delete()
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)

    


'''
class RecoverProjectView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Project")
    def put(self, request, deleteRecordId):
        
        project = get_object_or_404(Project, deleteRecord=deleteRecordId)
        isMember = UserTeam.objects.filter(team=project.belongTo, user =request.user).first() 
        if isMember:
            project.isDeleted=False
            project.save()
            allDocuments = Document.objects.filter(belongTo=project)
            for document in allDocuments:
                document.isDeleted=False
                document.save()
                #document.deleteRecord = null
            allDiagrams = Diagram.objects.filter(belongTo=project)
            for diagram in allDiagrams:
                diagram.isDeleted=False
                diagram.save()
                #diagram.deleteRecord = null
            deleteRecord = Deletion.objects.get(pk=deleteRecordId)
            deleteRecord.delete()
            return Response({"message": "Recover Project Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)


    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Project By Id")
    def delete(self, request, deleteRecordId):
        project = get_object_or_404(Project, deleteRecord=deleteRecordId)
        isMember = UserTeam.objects.filter(team=project.belongTo, user =request.user).first() 
        if isMember:
            project.delete()
            deleteRecord = Deletion.objects.get(pk=deleteRecordId)
            deleteRecord.delete()
            return Response({"message": "Delete Project Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)


class RecoverDocumentView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Document")
    def put(self, request, deleteRecordId):
        document = get_object_or_404(Document, deleteRecord=deleteRecordId)
        isMember = UserTeam.objects.filter(team=document.belongTo.belongTo, user =request.user).first() 
        if isMember:
            document.isDeleted=False
            document.save()
            #document.deleteRecord = null

            deleteRecord = Deletion.objects.get(pk=deleteRecordId)
            deleteRecord.delete()
            return Response({"message": "Recover Document Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)


    # Delete Project By Id
    @swagger_auto_schema(operation_summary="Delete Document By Id")
    def delete(self, request, deleteRecordId):
        document = get_object_or_404(Document, deleteRecord=deleteRecordId)
        isMember = UserTeam.objects.filter(team=document.belongTo.belongTo, user =request.user).first() 
        if isMember:
            document.delete()
            deleteRecord = Deletion.objects.get(pk=deleteRecordId)
            deleteRecord.delete()
            return Response({"message": "Delete Document Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)

class RecoverDiagramView(generics.GenericAPIView):
    serializer_class = RecoveryDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Update Project By Id
    @swagger_auto_schema(operation_summary="Recover Diagram")
    def put(self, request, deleteRecordId):
        diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
        isMember = UserTeam.objects.filter(team=diagram.belongTo.belongTo, user =request.user).first() 
        if isMember:
            
            diagram.isDeleted=False
            diagram.save()
            #diagram.deleteRecord = null

            deleteRecord = Deletion.objects.get(pk=deleteRecordId)
            deleteRecord.delete()
            return Response({"message": "Recover Diagram Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)

    # Delete Diagram By Id
    @swagger_auto_schema(operation_summary="Delete Diagram By Id")
    def delete(self, request, deleteRecordId):
        diagram = get_object_or_404(Diagram, deleteRecord=deleteRecordId)
        isMember = UserTeam.objects.filter(team=diagram.belongTo.belongTo, user =request.user).first() 
        if isMember:
            diagram.delete()
            deleteRecord = Deletion.objects.get(pk=deleteRecordId)
            deleteRecord.delete()
            return Response({"message": "Delete Diagram Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not team member"}, status=status.HTTP_401_UNAUTHORIZED)
'''
