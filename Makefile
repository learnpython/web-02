.PHONY: bootstrap clean distclean manage pep8 server

PROJECT = 
ENV ?= env
VENV := $(shell echo $(VIRTUAL_ENV))

ifneq ($(VENV),)
	PEP8 = pep8
	PYTHON = python
else
	PEP8 = $(ENV)/bin/pep8
	PYTHON = $(ENV)/bin/python
endif

HOST ?= 0.0.0.0
PORT ?= 8300

bootstrap:
	bootstrapper -e $(ENV)

clean:
	find . -name "*.pyc" -delete

distclean: clean
	rm -rf $(ENV)/ $(PROJECT)/settings_local.py

manage:
	$(PYTHON) manage.py $(COMMAND)

pep8:
	pep8 --statistics $(PROJECT)/

server:
	COMMAND="runserver_plus $(HOST):$(PORT)" $(MAKE) manage
