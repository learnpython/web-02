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
        verbose_name=_('feeds')
    )
    tags = models.ManyToManyField(
        'feeds.Tag', blank=True, null=True, related_name='users',
        verbose_name=_('tags')
    )

    class Meta:
        db_table = 'chitatel_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
