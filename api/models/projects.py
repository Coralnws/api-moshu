import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from .teams import Team
from ..utils import get_thumbnail

class Project(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    belongTo = models.ForeignKey("Team", on_delete=models.CASCADE, null=False, blank=False)
    deleteRecord = models.ForeignKey("Deletion", on_delete=models.SET_NULL, null=True, blank=True)
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
