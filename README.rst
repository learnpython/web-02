========
Chitatel
========

Google Reader clone built on top of Python 2.7 and Django 1.5.

Requirements
============

* `Python <http://www.python.org/>`_ 2.7
* `PostgreSQL <http://www.postgresql.org/>`_ 9.1 or higher
* `Make <http://www.gnu.org/software/make>`_
* `bootstrapper <http://pypi.python.org/pypi/bootstrapper>`_ 0.1.5 or higher

Installation
============

::

    $ make bootstrap
    $ make createdb
    $ make syncdb

Running
=======

Development web server
----------------------

::

    $ make devserver

Gunicorn web server
-------------------

::

    $ make server

Tests
-----

::

    $ make test
