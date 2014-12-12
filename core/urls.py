from django.conf.urls import patterns, include, url

from tastypie.api import Api
from apps.filehandler.api import OddlyFileHandling, TaskManagerEntry

from core.api.endpoints.item import ItemHandlingResource
from core.api.endpoints.artist import ArtistHandlingResource

urlpatterns = patterns('',
    url(r'^teapot/', include(ItemHandlingResource.urls())),
    url(r'^teapot/', include(ArtistHandlingResource.urls())),
                       
    url(r'^thumb/[0-9a-fA-F]{24}$', 'apps.filehandler.views.get_thumb', name='get_thumb')    
    )
