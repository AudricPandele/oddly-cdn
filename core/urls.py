from django.conf.urls import patterns, include, url

from tastypie.api import Api
from apps.filehandler.api import OddlyFileHandling 

'''
Tastypie ApiCdn
__version__ : v1

Register models :
    BetaccountEntry
    BookResource
'''

v1_api = Api(api_name = 'v1')
v1_api.register(OddlyFileHandling())


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls))
)
