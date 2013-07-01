# -*- coding: utf-8 -*-

from django.db.models import signals

from .models import Feed
from .tasks import reload_feed


def on_feed_update(*args, **kwargs):
    feed = kwargs['instance']

    if kwargs['created'] or feed.reloaded_at is None:
        reload_feed.apply_async(args=[feed.pk], countdown=4)
signals.post_save.connect(on_feed_update, sender=Feed)
