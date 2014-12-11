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
class ArtistHandlingResource(DjangoResource):
    
    #---------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(ArtistHandlingResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'thumbupload': {
                'POST': 'thumbupload',
            },
            'coverupload': {
                'POST': 'coverupload',
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
            cover_upload_path = "artist/covers/%s" % (mongoid)
            cover_save = default_storage.save(cover_upload_path, ContentFile(file_cover.read()))
            convert = self.convert_cover_to_jpeg(current_cover_path = "%sartist/covers/%s" % (settings.MEDIA_ROOT, mongoid),type_image = "covers", mongoid = mongoid)
        
        
    #---------------------------------------------------------------------------
    @skip_prepare
    def thumbupload(self):
        import pdb; pdb.set_trace()
        mongoid = None
        file_cover = None

        if self.data.get('file'):
            # Getting datas 
            file_cover = self.data.get('file')
            mongoid = self.data.get('_id')
            
        if file_cover is not None:
            # Actually upload then converting the cover
            cover_upload_path = "artist/thumbs/%s" % (mongoid)
            cover_save = default_storage.save(cover_upload_path, ContentFile(file_cover.read()))
            convert = self.convert_cover_to_jpeg(current_cover_path = "%sartist/thumbs/%s" % (settings.MEDIA_ROOT, mongoid), type_image = "thumbs", mongoid = mongoid)

    #---------------------------------------------------------------------------
    def convert_cover_to_jpeg(self, current_cover_path, mongoid, type_image):
        """
        Cover are not always jpeg, so we should convert the uploaded file to jpeg, uh
        """
        img = Image(str(current_cover_path))
        jpegwritepath = str("%sartist/%s/%s.jpg" % (settings.MEDIA_ROOT, type_image, mongoid))
        img.write(jpegwritepath)
        remove_tmp_file = os.remove("%sartist/%s/%s" % (settings.MEDIA_ROOT, type_image, mongoid))

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

        return super(ArtistHandlingResource, self).deserialize(method, endpoint, format)

    #---------------------------------------------------------------------------
    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(ArtistHandlingResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^thumbupload/$', csrf_exempt(cls.as_view('thumbupload')), name=cls.build_url_name('thumbupload', name_prefix)),
            url(r'^coverupload/$', csrf_exempt(cls.as_view('coverupload')), name=cls.build_url_name('coverupload', name_prefix)),
        )
