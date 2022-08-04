from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.invitations import Invitation

"""
Invitation
"""
class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'

    extra_kwargs = {
        'teamId': {'read_only': True},
        'user': {'read_only': True},
        'invitedBy': {'read_only': False},
        'createdAt': {'read_only': True},
        'updatedAt': {'read_only': True},
    }

class ReplyInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id']
