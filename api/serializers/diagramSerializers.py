from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.diagrams import *

"""
Serializer class for Diagram Detail
"""
class DiagramDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = ['id', 'title',  'componentData','canvasStyleData',  'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Diagram Profile (include rating, likes, dislikes)
"""
class DiagramProfileSerializer(serializers.ModelSerializer):
    # likes = serializers.IntegerField()
    # dislikes = serializers.IntegerField()
    # response = serializers.CharField()
    class Meta:
        model = Diagram
        fields = ['id', 'title',  'componentData','canvasStyleData', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Creating Diagram
"""
class DiagramCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = ['id','title', 'componentData','canvasStyleData']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Diagrams
"""
class ListDiagramSerializer(serializers.ModelSerializer):
    # likes = serializers.IntegerField()
    # dislikes = serializers.IntegerField()
    # reviewers = serializers.IntegerField()
    # response = serializers.CharField()
    class Meta:
        model = Diagram
        fields = ['id', 'title',  'componentData','canvasStyleData','isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id','img']

        extra_kwargs = {
            'id': {'read_only': True},
        }