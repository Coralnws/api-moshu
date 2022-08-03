from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.documents import Document

"""
Serializer class for Document Detail
"""
class DocumentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'content', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Document Profile (include rating, likes, dislikes)
"""
class DocumentProfileSerializer(serializers.ModelSerializer):
    # likes = serializers.IntegerField()
    # dislikes = serializers.IntegerField()
    # response = serializers.CharField()
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'content', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Creating Document
"""
class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','title', 'description', 'content']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Documents
"""
class ListDocumentSerializer(serializers.ModelSerializer):
    # likes = serializers.IntegerField()
    # dislikes = serializers.IntegerField()
    # reviewers = serializers.IntegerField()
    # response = serializers.CharField()
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']


# class ListTeamDocumentSerializer(serializers.ModelSerializer):
#     likes = serializers.IntegerField()
#     dislikes = serializers.IntegerField()
#     reviewers = serializers.IntegerField()
#     isPin = serializers.IntegerField()
#     isFeatured = serializers.IntegerField()
#     response = serializers.CharField()
#     class Meta:
#         model = Document
#         fields = ['id', 'title','description','createdBy', 'likes', 'dislikes', 'reviewers','createdAt','isPin','isFeatured','response']