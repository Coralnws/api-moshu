from django.db import models
from django.utils import timezone

#Team joined by user
class UserTeam(models.Model):
    team = models.ForeignKey("Team", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    isAdmin = models.BooleanField(default=False)
    isMainAdmin = models.BooleanField(default=False) #isCreator
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('team','user')


class UserProject(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    isAdmin = models.BooleanField(default=False)
    isMainAdmin = models.BooleanField(default=False) #isCreator
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('project','user')