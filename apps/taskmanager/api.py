import base64
import json
import requests
# tastypie
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.validation import Validation
from tastypie.exceptions import BadRequest

from django.conf import settings
# Import models
from apps.taskmanager.models import TaskManager


class TaskManagerEntry(ModelResource):
    id = fields.CharField(attribute="id")
    
    class Meta:
        queryset = TaskManager.objects.all()
        method = ["get"]
        resource_name="taskstatus"

    def object_list(self, request):
        status = TaskManager.objects.filter(book_id=request.GET.get('book_id'))
        if status:
            return status
        return False
