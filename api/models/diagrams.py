from pyexpat import model
import uuid
from django.utils import timezone
from django.db import models
from datetime import date
from .users import CustomUser
from .teams import Team
from ..utils import get_thumbnail

class Diagram(models.Model):

    data1 = '[{"animations":[],"events":{},"groupStyle":{},"isLock":false,"collapseName":"","linkage":{"duration":0,"data":[{"id":"","label":"","event":"","style":[{"key":"","value":""}]}]},"component":"VText","label":"文字","propValue":"这是一个画布","icon":"wenben","request":{"method":"GET","data":[],"url":"","series":false,"time":1000,"paramType":"","requestCount":0},"style":{"rotate":0,"opacity":1,"width":97,"height":28,"fontSize":"","fontWeight":400,"lineHeight":"","letterSpacing":0,"textAlign":"","color":"","top":193,"left":222},"id":"_udPGUKIdiUjAo6jsosQr"}]'
    data2 = '{"width":1920,"height":1020,"scale":100,"color":"#000","opacity":1,"background":"#fff","fontSize":14}'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=10000,null=True,blank=True)
    componentData = models.TextField(max_length=10000,null=True,blank=True,default=data1)
    canvasStyleData = models.TextField(max_length=10000,null=True,blank=True,default=data2)
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