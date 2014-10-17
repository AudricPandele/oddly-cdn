from django.db import models

class TaskManager(models.Model):
    
    book_id = models.CharField(
        max_length=255
        )

    process_status = models.CharField(
        max_length = 100
        )

