"""
==============
chitatel.utils
==============

Common helpers and utility functions to whole Chitatel project.

"""

import copy
import logging
import os

from distutils.util import strtobool

from werkzeug.utils import import_string


# Functions to read setting values from environment
BOOL = lambda value: (bool(strtobool(value))
                      if isinstance(value, basestring)
                      else value)
ENV = os.environ.get

# Absolute path to current directory and relative path builder function
DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *parts: os.path.abspath(os.path.join(DIRNAME, *parts))

# Default chitatel logger
logger = logging.getLogger('chitatel')


def dict_combine(first, second, do_copy=True):
    """
    Combine two dicts, but without affects to original dicts.
    """
    copied = copy.deepcopy(first) if do_copy else first

    for key, value in second.iteritems():
        exists = key in copied

        if exists and isinstance(copied[key], dict):
            assert isinstance(value, dict)
            copied[key] = dict_combine(copied[key], value)
        elif exists and isinstance(copied[key], list):
            assert isinstance(value, list)
            copied[key] = copied[key] + value
        elif exists and isinstance(copied[key], set):
            assert isinstance(value, set)
            copied[key] = copied[key] ^ value
        elif exists and isinstance(copied[key], tuple):
            assert isinstance(value, tuple)
            copied[key] = copied[key] + value
        else:
            copied[key] = value

    return copied


def import_settings(settings, context, fail_silently=False):
    """
    Import all possible settings from ``settings`` module and place them to
    ``context`` dict..

    If settings module doesn't exist, ``ImportError`` would be raised, but you
    should supress this approach by passing ``fail_silently=True``.
    """
    try:
        module = import_string(settings)
    except ImportError:
        if fail_silently:
            return False
        raise

    for attr in dir(module):
        if not attr.isupper() or attr.startswith('_'):
            continue
        context[attr] = getattr(module, attr)

    return True
