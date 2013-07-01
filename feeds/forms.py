# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


class FeedAdminForm(forms.ModelForm):
    reload_url = forms.BooleanField(label=_('Reload URL'), required=False)
