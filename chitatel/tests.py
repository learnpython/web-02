"""
==============
chitatel.tests
==============

Unit tests for chitatel application.

"""

import os

from django.test import TestCase

from . import settings
from .utils import BOOL, ENV, extra_combine, import_settings, logging_combine


class TestUtils(TestCase):

    def test_bool(self):
        self.assertTrue(BOOL(True))
        self.assertFalse(BOOL(False))
        self.assertTrue(BOOL(1))
        self.assertFalse(BOOL(0))
        self.assertTrue(BOOL('1'))
        self.assertFalse(BOOL('0'))
        self.assertTrue(BOOL('y'))
        self.assertFalse(BOOL('n'))
        self.assertTrue(BOOL('yes'))
        self.assertFalse(BOOL('no'))
        self.assertTrue(BOOL('True'))
        self.assertFalse(BOOL('False'))

    def test_env(self):
        self.assertEqual(ENV('USER'), os.environ['USER'])
        self.assertIsNone(ENV('DOES_NOT_EXIST'))

    def test_import_settings(self):
        data = {}
        import_settings('chitatel.settings', data)
        self.assertIn('DEBUG', data)

    def test_import_settings_fail_silently(self):
        data = {}
        import_settings('chitatel.does_not_exist', data, True)
        self.assertEqual(data, {})

    def test_settings(self):
        self.assertTrue(hasattr(settings, 'AUTH_USER_MODEL'))
        self.assertTrue(hasattr(settings, 'DEBUG'))
        self.assertFalse(hasattr(settings, 'DOES_NOT_EXIST'))
