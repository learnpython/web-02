"""
=============
chitatel.urls
=============

Base URL configuration for Chitatel project.

"""

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^feeds/', include('feeds.urls')),
    url(r'^users/', include('users.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
