"""
===========
users.admin
===========

Enable admin support for users application.

"""

from django.contrib import admin

from .models import User, UserTag, UserFeed


admin.site.register(User)
admin.site.register(UserTag)
admin.site.register(UserFeed)
