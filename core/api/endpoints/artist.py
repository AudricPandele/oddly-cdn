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

# Restless shit
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.resources import skip_prepare
from restless.exceptions import Unauthorized

# PDF processing
from apps.filehandler.models import FileHandler
from apps.filehandler import fileprocessing
from apps.taskmanager.models import TaskManager
from apps.filehandler.tasks import run_parser

# Image processing
from utils.tools import uploadImage


class ArtistHandlingResource(DjangoResource):


    def __init__(self, *args, **kwargs):
        super(ArtistHandlingResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'thumbupload': { 'POST': 'thumbupload' },
            'coverupload': { 'POST': 'coverupload' }
            })


    def is_authenticated(self):
        return True


    @skip_prepare
    def coverupload(self):
        uploadImage(
            file = self.data.get("file"),
            relativePath = str("artist/covers/%s" % (self.data.get("_id"))),
            absolutePath = "%sartist/covers/%s" %  (settings.MEDIA_ROOT, self.data.get("_id"))),
            extensionPath = "%sartist/covers/%s.jpg" %  (settings.MEDIA_ROOT, self.data.get("_id")))
        )


    @skip_prepare
    def thumbupload(self):
        uploadImage(
            file = self.data.get("file"),
            relativePath = str("artist/thumbs/%s" % (self.data.get("_id"))),
            absolutePath = "%sartist/thumbs/%s" %  (settings.MEDIA_ROOT, self.data.get("_id"))),
            extensionPath = "%sartist/thumbs/%s.jpg" %  (settings.MEDIA_ROOT, self.data.get("_id")))
        )


    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(ArtistHandlingResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^artist/thumb$', csrf_exempt(cls.as_view('thumbupload')), name=cls.build_url_name('thumbupload', name_prefix)),
            url(r'^artist/cover$', csrf_exempt(cls.as_view('coverupload')), name=cls.build_url_name('coverupload', name_prefix)),
            )
