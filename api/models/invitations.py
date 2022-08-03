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
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False,related_name='user_invite')
    team = models.ForeignKey("Team", on_delete=models.CASCADE, null=False, blank=False)
    invitedBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=True,blank=False,related_name='inviteBy')
    result = models.IntegerField(choices=RESULT,null=False, blank=False, default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)