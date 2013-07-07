"""
==========
feeds.urls
==========

URL configuration for feeds application.

"""

from django.conf.urls import patterns, url
from feeds.views import import_opml


urlpatterns = patterns(
    '',
    url(r'^import_opml/?$', import_opml),
)
