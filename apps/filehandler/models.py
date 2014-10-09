import os
from django.db import models
from django.conf import settings

class FileHandler(models.Model):

    uploaded_file = models.FileField(
        upload_to=settings.MEDIA_ROOT
        )
    class Meta:
        managed=None
        
    
