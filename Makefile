### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Python checks
UV?=uv

# installed?
ifeq (, $(shell which $(UV) ))
  $(error "UV=$(UV) not found in $(PATH)")
endif

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifdef PLONE_VERSION
PLONE_VERSION := $(PLONE_VERSION)
else
PLONE_VERSION := 6.1.4
endif

ifdef CI
UV_VENV_ARGS :=
else
UV_VENV_ARGS := --python=3.12
endif

VENV_FOLDER=$(BACKEND_FOLDER)/.venv
export VIRTUAL_ENV=$(VENV_FOLDER)
BIN_FOLDER=$(VENV_FOLDER)/bin

# Docs configuration
DOCS_SPHINXOPTS      ?=
DOCS_DIR=$(BACKEND_FOLDER)/docs
DOCS_BUILDDIR=$(DOCS_DIR)/_build
DOCS_VALEFILES       := $(shell find $(DOCS_DIR) -type f -name "*.md" -print)
DOCS_VALEOPTS        ?=

# Environment variables to be exported
export PYTHONWARNINGS := ignore
export DOCKER_BUILDKIT := 1

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

############################################
# Config
############################################
instance/etc/zope.ini instance/etc/zope.conf: ## Create instance configuration
	@echo "$(GREEN)==> Create instance configuration$(RESET)"
	@uvx cookiecutter -f --no-input -c 2.1.1 --config-file instance.yaml gh:plone/cookiecutter-zope-instance

.PHONY: config
config: instance/etc/zope.ini

############################################
# Install
############################################

requirements-mxdev.txt: pyproject.toml mx.ini ## Generate constraints file
	@echo "$(GREEN)==> Generate constraints file$(RESET)"
	@echo '-c https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt' > requirements.txt
	@uvx --from "mxdev[uv]" mxdev -c mx.ini
	@# plone-stubs is not on PyPI; install from git only on Python >= 3.12.
	@# The marker has to live here (not in pyproject.toml or mx.ini), since
	@# uv pip install does not honor [tool.uv.sources] when managed = false,
	@# and mxdev sections do not support PEP 508 markers per section.
	@echo "plone-stubs @ git+https://github.com/plone/plone-stubs.git ; python_version >= '3.12'" >> requirements-mxdev.txt

$(VENV_FOLDER): requirements-mxdev.txt ## Install dependencies
	@echo "$(GREEN)==> Install environment$(RESET)"
	@if [[ -d "$(VENV_FOLDER)" ]]; then echo "$(YELLOW)==> Environment already exists at $(VENV_FOLDER)$(RESET)"; else uv venv $(UV_VENV_ARGS) $(VENV_FOLDER); fi
	@uv pip install -r requirements-mxdev.txt

.PHONY: sync
sync: $(VENV_FOLDER) ## Sync project dependencies
	@echo "$(GREEN)==> Sync project dependencies$(RESET)"
	@uv pip install -r requirements-mxdev.txt

.PHONY: install
install: $(VENV_FOLDER) config ## Install Plone and dependencies

.PHONY: clean
clean: ## Clean installation and instance
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	@rm -rf $(VENV_FOLDER) pyvenv.cfg .installed.cfg instance .venv .pytest_cache .ruff_cache constraints* requirements*

.PHONY: remove-data
remove-data: ## Remove all content
	@echo "$(RED)==> Removing all content$(RESET)"
	rm -rf $(VENV_FOLDER) instance/var

############################################
# QA
############################################
.PHONY: mypy
mypy: ## Type checking
	@echo "$(GREEN)==> Run mypy$(RESET)"
	@uv run mypy src

.PHONY: lint
lint: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Lint codebase$(RESET)"
	@uvx ruff@latest check --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx pyroma@latest -d .
	@uvx check-python-versions@latest .
	@uvx zpretty@latest --check src
	@uv run mypy src

.PHONY: format
format: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	@uvx ruff@latest check --select I --fix --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx ruff@latest format --config $(BACKEND_FOLDER)/pyproject.toml
	@uvx zpretty@latest -i src

.PHONY: check
check: format lint ## Check and fix code base according to Plone standards

############################################
# Tests
############################################
.PHONY: test
test: $(VENV_FOLDER) ## run tests
	@uv run pytest

.PHONY: test-coverage
test-coverage: $(VENV_FOLDER) ## run tests with coverage
	@uv run pytest -n0 --cov=pytest_plone --cov-report term-missing

############################################
# Documentation
############################################
# sphinx-autodoc2 analyses the source statically and never imports the package,
# so building the docs needs neither Plone nor the test environment. It gets its
# own small virtualenv and takes seconds rather than minutes.
.PHONY: docs
docs: $(VENV_FOLDER) ## Build the documentation (warnings are errors)
	@echo "$(GREEN)==> Build documentation$(RESET)"
	@$(VENV_FOLDER)/bin/sphinx-build -W --keep-going -b html $(DOCS_DIR) "$(DOCS_BUILDDIR)/html"

.PHONY: docs-livehtml
docs-livehtml: $(VENV_FOLDER)  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	@$(VENV_FOLDER)/bin/sphinx-autobuild \
		--ignore "*.swp" \
		--port 8050 \
		-b html $(DOCS_DIR) "$(DOCS_BUILDDIR)/html" $(DOCS_SPHINXOPTS)

.PHONY: docs-linkcheck
docs-linkcheck: $(VENV_FOLDER) ## Check that all links in the documentation resolve
	@echo "$(GREEN)==> Check documentation links$(RESET)"
	@$(VENV_FOLDER)/bin/sphinx-build -b linkcheck $(DOCS_DIR) "$(DOCS_BUILDDIR)/linkcheck"

.PHONY: docs-vale
docs-vale: $(VENV_FOLDER) ## Check the documentation with Vale
	@echo "$(GREEN)==> Check documentation with Vale$(RESET)"
	@$(VENV_FOLDER)/bin/vale sync
	@$(VENV_FOLDER)/bin/vale --no-wrap $(DOCS_VALEOPTS) $(DOCS_VALEFILES)

.PHONY: docs-clean
docs-clean: ## Remove the built documentation and its environment
	@echo "$(RED)==> Clean documentation$(RESET)"
	@rm -rf $(DOCS_BUILDDIR)

############################################
# Release
############################################
.PHONY: changelog
changelog: ## Release the package to pypi.org
	@echo "🚀 Display the draft for the changelog"
	@uv run towncrier --draft

.PHONY: release
release: ## Release the package to pypi.org
	@echo "🚀 Release package"
	@uv run prerelease
	@uv run release
	@rm -Rf dist
	@uv build
	@uv publish
	@uv run postrelease
