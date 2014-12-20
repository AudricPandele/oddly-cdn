from django.db import models

class TaskManager(models.Model):
    
    book_id = models.CharField(
        max_length=255
        )

    progress = models.CharField(
        max_length = 100
        )
    
    status = models.CharField(
        max_length = 100
        )

    current = models.CharField(
        max_length=50
        )

    total = models.CharField(
        max_length=50
        )
