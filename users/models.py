"""
============
users.models
============

Implementation of user model for Chitatel project.

"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    User model inherited from Django standard one, but with adding custom
    fields and relations.
    """
    feeds = models.ManyToManyField(
        'feeds.Feed', blank=True, null=True, related_name='users',
        verbose_name=_('feeds'),
        through='UserFeed'
    )
    tags = models.ManyToManyField(
        'feeds.Tag', blank=True, null=True, related_name='users',
        verbose_name=_('tags'),
        through='UserTag'
    )

    class Meta:
        db_table = 'chitatel_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserTag(models.Model):
    tag = models.ForeignKey('feeds.Tag', related_name='user_tags')
    user = models.ForeignKey(User, related_name='user_tags')
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='tags'
    )

    class Meta:
        db_table = 'chitatel_users_tags'
        verbose_name = _('user_tag')
        verbose_name_plural = _('user_tag')

    def __unicode__(self):
        """
        Unicode representation.
        """
        return u"%s - %s" % (self.user, self.tag)


class UserFeed(models.Model):
    feed = models.ForeignKey('feeds.Feed')
    user = models.ForeignKey(User)
    parent = models.ForeignKey(
        UserTag, null=True, blank=True, related_name='user_tags'
    )

    class Meta:
        db_table = 'chitatel_users_feeds'
        verbose_name = _('user_feed')
        verbose_name_plural = _('user_feed')

    def __unicode__(self):
        """
        Unicode representation.
        """
        return u"%s - %s" % (self.user, self.feed)
