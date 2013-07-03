.PHONY: bootstrap clean createdb devserver distclean manage pep8 server shell syncdb test

PROJECT = chitatel
APPS = feeds users
ENV ?= env
VENV := $(shell echo $(VIRTUAL_ENV))

ifneq ($(VENV),)
	HONCHO = honcho
	PEP8 = flake8
	PYTHON = python
else
	HONCHO = source $(ENV)/bin/activate && honcho
	PEP8 = $(ENV)/bin/flake8
	PYTHON = $(ENV)/bin/python
endif

HOST ?= 0.0.0.0
PORT ?= 8300
TEST_ARGS ?=

bootstrap:
	bootstrapper -e $(ENV)

clean:
	find . -name "*.pyc" -delete

createdb:
	createuser -s -P chitatel
	createdb -U chitatel chitatel

devserver: pep8
	PORT=$(PORT) $(HONCHO) start dev

distclean: clean
	rm -rf $(ENV)/ $(PROJECT)/settings_local.py

manage:
	$(PYTHON) manage.py $(COMMAND)

pep8:
	$(PEP8) --exclude=migrations --statistics $(PROJECT) $(APPS)

server: pep8
	PORT=$(PORT) $(HONCHO) start web

shell:
	COMMAND=shell_plus $(MAKE) manage

syncdb:
	COMMAND="syncdb --noinput" $(MAKE) manage
	COMMAND="migrate --noinput" $(MAKE) manage

test: pep8
	COMMAND="test $(TEST_ARGS) $(PROJECT) $(APPS)" $(MAKE) manage
