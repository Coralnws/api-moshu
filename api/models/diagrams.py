from pyexpat import model
import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from .teams import Team
from ..utils import get_thumbnail

class Diagram(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=10000,null=True,blank=True)
    #componentData = models.JSONField(null=True)
    componentData = models.TextField(max_length=10000)
    canvasStyleData = models.TextField(max_length=10000)
    #canvasStyleData = models.JSONField(null=True)
    content = models.JSONField(null=True,blank=True)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    belongTo = models.ForeignKey("Project", on_delete=models.CASCADE, null=False, blank=False)
    deleteRecord = models.ForeignKey("Deletion", on_delete=models.SET_NULL, null=True, blank=True)
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.ImageField(upload_to="uploads/imageUpload", blank=True)

    def save(self, *args, **kwargs):
        if self.img:
            # ratio 1:1
            self.img = get_thumbnail(self.img, 100, False, 1)     # quality = 100, isThumbnail False = maxWidthHeight = 1024px
        super(Image, self).save(*args, **kwargs)