import uuid
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
<<<<<<< HEAD
    description = models.TextField(max_length=50000)
    content = models.TextField()
=======
    description = models.TextField(max_length=10000)
    content = models.TextField(max_length=50000)
>>>>>>> e1d79165950d9ba80e2a5b32c158d4a463ae09eb
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    belongTo = models.ForeignKey("Project", on_delete=models.CASCADE, null=False, blank=False)
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)