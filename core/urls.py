from django.conf.urls import patterns, include, url

from tastypie.api import Api
from apps.filehandler.api import OddlyFileHandling, TaskManagerEntry

from core.api.endpoints.item import ItemHandlingResource
from core.api.endpoints.artist import ArtistHandlingResource

from core.api.endpoints.process import ProcessResource

urlpatterns = patterns('',
    url(r'^teapot/', include(ItemHandlingResource.urls())),
    url(r'^teapot/', include(ArtistHandlingResource.urls())),

    url(r'^artist/thumb/([0-9a-fA-F]{24})/([a-z]{,6})$', 'apps.filehandler.views.artist_thumb', name='artist_thumb'),
    url(r'^artist/cover/([0-9a-fA-F]{24})/([a-z]{,6})$', 'apps.filehandler.views.artist_cover', name='artist_cover'),

    url(r'^item/([0-9a-fA-F]{24})/([A-Z]{2})/([0-9]+)$', 'apps.filehandler.views.item_file', name='item_file'),
    url(r'^item/cover/([0-9a-fA-F]{24})/([a-z]{,6})$', 'apps.filehandler.views.item_cover', name='item_cover'),
    url(r'^item/background/([0-9a-fA-F]{24})/([a-z]{,6})$', 'apps.filehandler.views.item_background', name='item_background'),
    url(r'^', include(ProcessResource.urls())),
    )
