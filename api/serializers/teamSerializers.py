from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.teams import Team
from ..models.userRelations import UserTeam
from ..models.invitations import Invitation

"""
Team Detail - For update or delete
"""
class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'teamName', 'description','createdBy']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
        }


"""
Getting Team Info
"""
#include member
class TeamProfileSerializer(serializers.ModelSerializer):
    members = serializers.IntegerField()
    class Meta:
        model = Team
        fields = ['id', 'teamName', 'description', 'createdBy', 'members','createdAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
        }



"""
Create Team
"""
class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','teamName', 'description','img']
        
    def validate(self, attrs):
        return super().validate(attrs)

"""
List All Team
"""
class ListTeamSerializer(serializers.ModelSerializer):
    members = serializers.IntegerField()
    joinedAt = serializers.DateTimeField()
    position = serializers.CharField(max_length=20)
    class Meta:
        model = Team
        fields = ['id', 'teamName', 'description', 'createdBy', 'members','createdAt','joinedAt','position']


class UserTeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeam
        fields = '__all__'
        extra_kwargs = {
            'team': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

"""
Add userTeam relation
"""
class UserTeamJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeam
        fields = ['user','team']

    def validate(self, attrs):
        return super().validate(attrs)






