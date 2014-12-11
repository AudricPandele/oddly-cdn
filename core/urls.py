from django.conf.urls import patterns, include, url

from tastypie.api import Api
from apps.filehandler.api import OddlyFileHandling, TaskManagerEntry

from core.api.endpoints.item import ItemHandlingResource
from core.api.endpoints.artist import ArtistHandlingResource

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(ItemHandlingResource.urls())),
    url(r'^api/v1/', include(ArtistHandlingResource.urls())),
    url(r'^thumb/[0-9a-fA-F]{24}$', 'apps.filehandler.views.get_thumb', name='get_thumb')
    
)
