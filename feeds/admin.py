# -*- coding: utf-8 -*-

"""
===========
feeds.admin
===========

Enable admin support for feed application.

"""

from django.contrib import admin

from .models import Feed, Entry, Tag
from .forms import FeedAdminForm


class FeedAdmin(admin.ModelAdmin):
    form = FeedAdminForm
    list_display = ('_title', 'url', 'reloaded_at')
    readonly_fields = ('reloaded_at', '_dict',)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['reload_url']:
            obj.reload()
        else:
            obj.save()
admin.site.register(Feed, FeedAdmin)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('feed', '_title', '_link')
    list_display_links = ('_title',)
    readonly_fields = ('feed', '_title', '_dict',)
admin.site.register(Entry, EntryAdmin)


admin.site.register(Tag)
