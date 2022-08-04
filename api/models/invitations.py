import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from .teams import Team
from ..utils import get_thumbnail

class Invitation(models.Model):
    RESULT = (
        (0, 'Pending'),
        (1, 'Accept'),
        (2, 'Decline'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=150)
    team = models.CharField(max_length=150,null=True)
    teamId = models.ForeignKey("Team", on_delete=models.CASCADE, null=True, blank=False)
    teamImg = models.ImageField(upload_to="uploads/teams", blank=True)
    invitedBy = models.CharField(max_length=150)
    result = models.IntegerField(choices=RESULT,null=False, blank=False, default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    