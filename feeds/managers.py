# -*- coding: utf-8 -*-

from django.db import models


class FeedManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return super(
            FeedManager, self
        ).get_query_set(*args, **kwargs).defer('_dict')


class EntryManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return super(
            EntryManager, self
        ).get_query_set(
            *args, **kwargs
        ).defer('_dict').prefetch_related('feed')
