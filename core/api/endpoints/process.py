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
class ProcessResource(DjangoResource):
    
    #---------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(ProcessResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'processdetail': {
                'GET': 'processdetail',
            },
        })

    #---------------------------------------------------------------------------
    def is_authenticated(self):
        return True
            
    #---------------------------------------------------------------------------
    @skip_prepare
    def processdetail(self, mongoid):
        progress = TaskManager.objects.get(book_id=mongoid)
        return {
            "progress":progress.progress,
            "status":progress.status,
            "current":progress.current,
            "total":progress.total,

            }
        
    #---------------------------------------------------------------------------
    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(ProcessResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^progress/([0-9a-fA-F]{24})$', csrf_exempt(cls.as_view('processdetail')), name=cls.build_url_name('processdetail', name_prefix)),
        )
