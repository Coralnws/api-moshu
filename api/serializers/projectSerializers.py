from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.projects import Project

"""
Serializer class for Project Detail
"""
class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Project Profile (include rating, likes, dislikes)
"""
class ProjectProfileSerializer(serializers.ModelSerializer):
    # likes = serializers.IntegerField()
    # dislikes = serializers.IntegerField()
    # response = serializers.CharField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Creating Project
"""
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','title', 'description']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Projects
"""
class ListProjectSerializer(serializers.ModelSerializer):
    # likes = serializers.IntegerField()
    # dislikes = serializers.IntegerField()
    # reviewers = serializers.IntegerField()
    # response = serializers.CharField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']


# class ListTeamProjectSerializer(serializers.ModelSerializer):
#     likes = serializers.IntegerField()
#     dislikes = serializers.IntegerField()
#     reviewers = serializers.IntegerField()
#     isPin = serializers.IntegerField()
#     isFeatured = serializers.IntegerField()
#     response = serializers.CharField()
#     class Meta:
#         model = Project
#         fields = ['id', 'title','description','createdBy', 'likes', 'dislikes', 'reviewers','createdAt','isPin','isFeatured','response']