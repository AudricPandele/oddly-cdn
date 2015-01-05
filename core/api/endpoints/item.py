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

#---------------------------------------------------------------------------
class ItemHandlingResource(DjangoResource):

    #---------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(ItemHandlingResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'fileupload': {
                'POST': 'fileupload',
            },
            'coverupload': {
                'POST': 'coverupload',
            },
            'backgroundupload': {
                'POST': 'backgroundupload',
            }
        })

    #---------------------------------------------------------------------------
    def is_authenticated(self):
        return True

    #---------------------------------------------------------------------------
    @skip_prepare
    def coverupload(self):
        mongoid = None
        file_cover = None

        if self.data.get('file'):
            # Getting datas
            file_cover = self.data.get('file')
            mongoid = self.data.get('_id')

        if file_cover is not None:
            # Actually upload then converting the cover
            cover_upload_path = "items/covers/%s" % (mongoid)
            cover_save = default_storage.save(cover_upload_path, ContentFile(file_cover.read()))
            convert = self.convert_cover_to_jpeg(current_cover_path = "%sitems/covers/%s" % (settings.MEDIA_ROOT, mongoid), mongoid = mongoid)

    #---------------------------------------------------------------------------
    @skip_prepare
    def backgroundupload(self):
        mongoid = None
        file_background = None

        if self.data.get('file'):
            file_background = self.data.get('file')
            mongoid = self.data.get('_id')

        if file_background is not None:
            bg_upload_path = "items/backgrounds/%s" % (mongoid)
            bg_save = default_storage.save(bg_upload_path, ContentFile(file_background.read()))
            convert = self.convert_bg_to_jpeg(current_bg_path = "%items/backgrounds/%s" % (settings.MEDIA_ROOT, mongoid), mongoid = mongoid)

    #---------------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
    def convert_cover_to_jpeg(self, current_cover_path, mongoid):
        """
        Cover are not always jpeg, so we should convert the uploaded file to jpeg, uh
        """
        img = Image(str(current_cover_path))
        jpegwritepath = str("%sitems/covers/%s.jpg" % (settings.MEDIA_ROOT, mongoid))
        img.write(jpegwritepath)
        remove_tmp_file = os.remove("%sitems/covers/%s" % (settings.MEDIA_ROOT, mongoid))

    def convert_bg_to_jpeg(self, current_bg_path, mongoid):
        img = Image(str(current_bg_path))
        jpegwritepath = str("%sitems/backgrounds/%s.jpg" % (settings.MEDIA_ROOT, mongoid))
        img.write(jpegwritepath)
        remove_tmp_file = os.remove("%sitems/backgrounds/%s" % (settings.MEDIA_ROOT, mongoid))

    #---------------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(ItemHandlingResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^item/pdf/$', csrf_exempt(cls.as_view('fileupload')), name=cls.build_url_name('fileupload', name_prefix)),
            url(r'^item/cover/$', csrf_exempt(cls.as_view('coverupload')), name=cls.build_url_name('coverupload', name_prefix)),
            url(r'^item/background/$', csrf_exempt(cls.as_view('backgroundupload')), name=cls.build_url_name('backgroundupload', name_prefix))
        )
