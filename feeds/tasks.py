# -*- coding: utf-8 -*-

from datetime import timedelta

from django.utils.timezone import now

from djcelery import celery

from .models import Feed


def get_eta(http_headers):
    # TODO
    return now() + timedelta(minutes=32)


@celery.task
def reload_feed(pk):
    try:
        feed = Feed.objects_with_deferred_dict.get(pk=pk)
    except Feed.DoesNotExist:
        return

    http_headers = feed.reload()
    eta = get_eta(http_headers)
    reload_feed.apply_async(args=[feed.pk], eta=eta)
