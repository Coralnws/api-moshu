import uuid
import json
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from .teams import Team
from .projects import Project
from ..utils import get_thumbnail

class Document(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=10000,null=True,blank=True)
    content = models.TextField(null=True, blank=True)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    belongTo = models.ForeignKey("Project", on_delete=models.CASCADE, null=True, blank=True)
    isPublic = models.BooleanField(default=True)
    version = models.IntegerField(default=0)
    deleteRecord = models.ForeignKey("Deletion", on_delete=models.SET_NULL, null=True, blank=True)
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)


class DocumentChange(models.Model):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, null=False, blank=False)
    version = models.IntegerField(default=0, db_index=True)
    requestId = models.CharField(max_length=64, unique=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    parentVersion = models.IntegerField(default=0)
    data = models.TextField()

    class Meta:
        unique_together = (
            ('document', 'version'),
            ('document', 'requestId', 'parentVersion'),
        )

    def export(self):
        out = {}
        out['version'] = self.version
        out['time'] = self.time.isoformat()
        out['op'] = json.loads(self.data)
        return out
