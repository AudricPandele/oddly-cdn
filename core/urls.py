from django.conf.urls import patterns, include, url

from apps.exampleapp import views as exampleview
from apps.exampleapp.api import EntryResource
from apps.betaccount.api import BetaccountEntry

entry_resource = EntryResource()
betaccount_resource = BetaccountEntry()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^example/',exampleview.test),
    url(r'^api/', include(entry_resource.urls)),
    url(r'^beta/', include(betaccount_resource.urls)),
)
