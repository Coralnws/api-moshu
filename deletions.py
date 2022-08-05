from pyexpat import model
import uuid
from django.utils import timezone
from django.db import models


class Diagram(models.Model):
    RESULT = (
        (0, 'Project'),
        (1, 'Document'),
        (2, 'Diagram'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    deletedBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    belongTo = models.ForeignKey("Team", on_delete=models.CASCADE, null=False, blank=False)
    type = models.IntegerField(choices=RESULT,null=False, blank=False)
    #includeFile = models.IntegerField(null=True,blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)