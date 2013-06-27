"""
===========
feeds.admin
===========

Enable admin support for feed application.

"""

from django.contrib import admin

from .models import Entry, Feed, Tag


admin.site.register(Entry)
admin.site.register(Feed)
admin.site.register(Tag)
