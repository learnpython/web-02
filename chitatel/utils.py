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


def extra_combine(base, extra):
    """
    Combine base and extra dicts which would be passed to extra log record
    method.
    """
    copied = copy.deepcopy(base)
    copied.update(extra)
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


def logging_combine(base, local):
    """
    Combine two logging config dictionaris.
    """
    copied = copy.deepcopy(base)

    for key, value in local.iteritems():
        if isinstance(copied[key], dict):
            assert isinstance(value, dict)
            copied[key] = logging_combine(copied[key], value)
        elif isinstance(copied[key], list):
            assert isinstance(value, list)
            copied[key] = copied[key] + value
        else:
            copied[key] = value

    return copied
