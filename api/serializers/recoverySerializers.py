from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.deletions import *

"""
Serializer class for Diagram Detail
"""
class RecoveryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deletion
        fields = ['id']

class ListRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deletion
        fields = ['id','title','deletedBy','belongTo','type']


