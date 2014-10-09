import os
from django.db import models

class FileHandler(models.Model):

    uploaded_file = models.FileField(
        upload_to="/"
        )
    class Meta:
        managed=None

