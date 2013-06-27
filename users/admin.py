"""
===========
users.admin
===========

Enable admin support for users application.

"""

from django.contrib import admin

from .models import User


admin.site.register(User)
