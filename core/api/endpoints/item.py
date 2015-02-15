# Python shit
import base64
import json
import requests
import os

# Django shit
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, url
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# RESTless shit
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.resources import skip_prepare
from restless.exceptions import Unauthorized

# Images processing
from utils.tools import uploadImage

# PDF processing
from apps.filehandler.models import FileHandler
from apps.filehandler import fileprocessing
from apps.taskmanager.models import TaskManager
from apps.filehandler.tasks import run_parser


class ItemHandlingResource(DjangoResource):


    def __init__(self, *args, **kwargs):
        super(ItemHandlingResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'fileupload': { 'POST': 'fileupload' },
            'coverupload': { 'POST': 'coverupload' },
            'backgroundupload': { 'POST': 'backgroundupload' }
            })


    def is_authenticated(self):
        return True


    @skip_prepare
    def coverupload(self):
        uploadImage(
            file = self.data.get("file"),
            relativePath = str("items/covers/%s" % (self.data.get("_id"))),
            absolutePath = str("%sitems/covers/%s" % (settings.MEDIA_ROOT, self.data.get("_id"))),
            extensionPath = str("%sitems/covers/%s.jpg" % (settings.MEDIA_ROOT, self.data.get("_id"))),
            )


    @skip_prepare
    def backgroundupload(self):
        uploadImage(
            file = self.data.get("file"),
            relativePath = str("items/backgrounds/%s" % (self.data.get("_id"))),
            absolutePath = str("%sitems/backgrounds/%s" % (settings.MEDIA_ROOT, self.data.get("_id"))),
            extentionPath = str("%sitems/backgrounds/%s.jpg" % (settings.MEDIA_ROOT, self.data.get("_id"))),
            )


    @skip_prepare
    def fileupload(self):

        mongoid = None
        file_pdf = None

        # Getting datas
        if self.data.get('_id'):
            mongoid = self.data.get('_id')
        if self.data.get('file'):
            file_pdf = self.data.get('file')

        upload_path = "items/pdf/original/%s/%s" % (mongoid, file_pdf.name)
        path = default_storage.save(upload_path, ContentFile(file_pdf.read()))

        if path:
            # Uploading and splitting the item
            uploaded_file = "%s%s" % (settings.MEDIA_ROOT, upload_path)
            run_parser.delay(uploaded_file=uploaded_file, mongo_id=mongoid)

    def deserialize(self, method, endpoint, body):
        format = None
        """
        Changes request stat in to python objects
        """
        if not format:
            format = self.request.META.get('CONTENT_TYPE', 'application/json')
            
        if format == 'application/x-www-form-urlencoded':
            return self.request.POST
        
        if format.startswith('multipart'):
            multipart_data = self.request.POST.copy()
            multipart_data.update(self.request.FILES)
            return multipart_data

        return super(ArtistHandlingResource, self).deserialize(method, endpoint, format)

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(ItemHandlingResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^item/pdf$', csrf_exempt(cls.as_view('fileupload')), name=cls.build_url_name('fileupload', name_prefix)),
            url(r'^item/cover$', csrf_exempt(cls.as_view('coverupload')), name=cls.build_url_name('coverupload', name_prefix)),
            url(r'^item/background$', csrf_exempt(cls.as_view('backgroundupload')), name=cls.build_url_name('backgroundupload', name_prefix))
            )
