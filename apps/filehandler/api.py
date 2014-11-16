# -*- coding: utf-8 -*-
import base64
import json
import requests
import os
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

from apps.filehandler.tasks import run_parser

from pgmagick import Image

class TaskManagerEntry(ModelResource):
    id = fields.CharField(attribute="id")
    class Meta:
        queryset = TaskManager.objects.all()
        method = ["get"]
        resource_name = 'taskstatus'
        filtering = {
            "book_id": ['exact'],
        }
    
class OddlyFileHandling(ModelResource):
    id = fields.CharField(attribute="id")
    class Meta:
        queryset = FileHandler.objects.all()
        method = ['post']
        resource_name = "fileupload"

    def obj_create(self, request):
        mongoid = request.data.get('itemid')
        file_pdf = request.data.get('file_pdf')
        file_thumb = request.data.get('file_thumb')
        upload_path = "%s/%s" % (mongoid, request.data.get('file_pdf').name)
        thumb_upload_path = "thumbs/%s" % (mongoid)
        thumb_save = default_storage.save(thumb_upload_path, ContentFile(file_thumb.read()))
        convert = self.convert_thumb_to_jpeg(current_thumb_path = "%sthumbs/%s" % (settings.MEDIA_ROOT, mongoid), mongoid = mongoid)
        path = default_storage.save(upload_path, ContentFile(file_pdf.read()))
        if path:
            uploaded_file = "%s%s" % (settings.MEDIA_ROOT, upload_path)
            run_parser.delay(uploaded_file=uploaded_file, mongo_id=mongoid)
            #fileprocessing.main(uploaded_file=uploaded_file, mongo_id=mongoid)

    def convert_thumb_to_jpeg(self, current_thumb_path, mongoid):
        img = Image(str(current_thumb_path))
        jpegwritepath = str("%sthumbs/%s.jpg" % (settings.MEDIA_ROOT, mongoid))
        img.write(jpegwritepath)
        remove_tmp_file = os.remove("%sthumbs/%s" % (settings.MEDIA_ROOT, mongoid))
        
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

