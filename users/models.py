"""
============
users.models
============

Implementation of user model for Chitatel project.

"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User model inherited from Django standard one, but with adding custom
    fields and relations.
    """
