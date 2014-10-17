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


# Import django validators and exceptions
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.conf import settings
# Import models
from apps.filehandler.models import FileHandler
from apps.filehandler import fileprocessing
#Import OddlyCustomBackends
#from core.api.oddlyauth import OddlyAuthentication
from apps.taskmanager.models import TaskManager


class TaskManagerEntry(ModelResource):
    id = fields.CharField(attribute="id")
    
    class Meta:
        queryset = TaskManager.objects.all()
        method = ["get"]


    def object_list(self, request):
        status = TaskManager.objects.filter(book_id=request.GET.get('book_id'))
        if status:
            return status
        return False

class OddlyFileHandling(ModelResource):
    id = fields.CharField(attribute="id")
    class Meta:
        queryset = FileHandler.objects.all()
        method = ['post']
        resource_name = "fileupload"

    def obj_create(self, request):
        mongoid = request.data.get('bookid')
        file = request.data.get('file')
        upload_path = "%s/%s" % (mongoid, request.data.get('file').name)
        path = default_storage.save(upload_path, ContentFile(file.read()))
        if path:
            uploaded_file = "%s%s" % (settings.MEDIA_ROOT, upload_path)
            fileprocessing.main(uploaded_file, mongoid)
    
    def deserialize(self, request, data, format=None):
        """
        Changes request stat in to python objects
        """
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
                return request.POST

        if format.startswith('multipart'):
            multipart_data = request.POST.copy()
            multipart_data.update(request.FILES)
            return multipart_data

        return super(OddlyFileHandling, self).deserialize(request, data, format)


class TaskManagerEntry(ModelResource):
    id = fields.CharField(attribute="id")
    
    class Meta:
        queryset = TaskManager.objects.all()
        method = ["get"]


    def object_list(self, request):
        status = TaskManager.objects.filter(book_id=request.GET.get('book_id'))
        if status:
            return status
        return False
