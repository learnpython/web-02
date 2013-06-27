"""
============
feeds.models
============

Implement core models for Chitatel project: feed, entry and tag.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Feed(models.Model):
    """
    Feed model.

    Save basic information about feed, like URL, title, short description.
    """
    title = models.CharField(_('title'), max_length=128)
    href = models.URLField(
        _('href'), max_length=255, unique=True, help_text=_('Feed href.')
    )
    link = models.URLField(
        _('link'), blank=True, max_length=255,
        help_text=_('Feed link, in most cases URL of site which produces '
                    'feed.')
    )
    summary = models.TextField(_('summary'), blank=True)

    update_date = models.DateTimeField(_('updated at'), blank=True, null=True)

    class Meta:
        db_table = 'chitatel_feed'
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')


class Entry(models.Model):
    """
    Entry model.

    Save all necessary information about feed entry.
    """
    feed = models.ForeignKey(
        Feed, related_name='entries', verbose_name=_('feed')
    )
    uid = models.CharField(_('UID'), max_length=255)

    title = models.CharField(_('title'), max_length=128)
    link = models.URLField(_('link'), max_length=255)
    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'), blank=True)

    publish_date = models.DateTimeField(_('published at'))
    update_date = models.DateTimeField(_('updated at'), blank=True, null=True)

    class Meta:
        db_table = 'chitatel_entry'
        unique_together = ('feed', 'uid')
        verbose_name = _('entry')
        verbose_name_plural = _('entries')


class Tag(models.Model):
    """
    Tag model.

    For now save here only tag name as primary key.
    """
    name = models.CharField(
        _('name'), max_length=32, primary_key=True, unique=True
    )

    class Meta:
        db_table = 'chitatel_tag'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __unicode__(self):
        """
        Unicode representation.
        """
        return self.name
