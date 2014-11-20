import base64
import json
import requests
import os

from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, url
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.resources import skip_prepare
from restless.exceptions import Unauthorized

# Import models
from apps.filehandler.models import FileHandler
from apps.filehandler import fileprocessing

from apps.taskmanager.models import TaskManager

from apps.filehandler.tasks import run_parser

from pgmagick import Image

class ItemHandlingResource(DjangoResource):

    def __init__(self, *args, **kwargs):
        super(ItemHandlingResource, self).__init__(*args, **kwargs)

        # Add on a new top-level key, then define what HTTP methods it
        # listens on & what methods it calls for them.
        self.http_methods.update({
            'fileupload': {
                'POST': 'fileupload',
            }
        })

    #Controls what data is included in the serialized output.
    preparer = FieldsPreparer(fields={
        'name': 'name',
        'description': 'description',
    })
    
    def is_authenticated(self):
        return True
    
    # GET /register
    def list(self):
        return Item.objects.all()

    # POST
    def create(self):
        Item.objects.create()
        

    @skip_prepare
    def fileupload(self):
        mongoid = self.data['itemid']
        file_pdf = self.data['file_pdf']
        file_thumb = self.data['file_thumb']
        upload_path = "%s/%s" % (mongoid, file_pdf.name)
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

        return super(ItemHandlingResource, self).deserialize(method, endpoint, format)

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(ItemHandlingResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^fileupload/$', csrf_exempt(cls.as_view('fileupload')), name=cls.build_url_name('fileupload', name_prefix)),
        )
