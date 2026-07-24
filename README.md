<h1 align="center">pytest-plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Status](https://img.shields.io/pypi/status/pytest-plone)](https://pypi.org/project/pytest-plone/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/pytest-plone)](https://pypi.org/project/pytest-plone/)

[![Tests](https://github.com/plone/pytest-plone/actions/workflows/ci.yml/badge.svg)](https://github.com/plone/pytest-plone/actions/workflows/ci.yml)

![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/plone/pytest-plone)](https://github.com/plone/pytest-plone)
[![GitHub Repo stars](https://img.shields.io/github/stars/plone/pytest-plone?style=social)](https://github.com/plone/pytest-plone)
</div>

**pytest-plone** is a [pytest](https://docs.pytest.org) plugin providing fixtures and helpers to test [Plone](https://plone.org) add-ons.
It builds on [zope.pytestlayer](https://github.com/zopefoundation/zope.pytestlayer), turning the `plone.testing` layers you already have into pytest fixtures.

📖 **Documentation: [plone.github.io/pytest-plone](https://plone.github.io/pytest-plone/)**

## Installation

```shell
pip install pytest-plone
```

## Quickstart

In your top-level `conftest.py`, import your testing layers and hand them to `fixtures_factory` with a prefix for each:

```python
from my.addon.testing import MY_ADDON_FUNCTIONAL_TESTING
from my.addon.testing import MY_ADDON_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (MY_ADDON_FUNCTIONAL_TESTING, "functional"),
        (MY_ADDON_INTEGRATION_TESTING, "integration"),
    ))
)
```

Then write tests as plain functions that ask for what they need:

```python
def test_portal_title(portal):
    assert portal.title == "Plone site"
```

Run them with `pytest`.

The [documentation](https://plone.github.io/pytest-plone/) covers the rest:

- [Write your first test](https://plone.github.io/pytest-plone/tutorials/first-test.html) — a guided start for a new add-on.
- [How-to guides](https://plone.github.io/pytest-plone/how-to/index.html) — set up the plugin, test add-on install, test a REST API, speed up a slow suite.
- [Fixtures reference](https://plone.github.io/pytest-plone/reference/fixtures.html) — every fixture, the `@pytest.mark.portal` marker, and the `fixtures_factory` API.
- [Testing layers, scopes, and isolation](https://plone.github.io/pytest-plone/explanation/layers-scopes-and-isolation.html) — how it all fits together.

## Contributing

You need a working Python environment, version 3.10 or later.

Install a development environment and run the tests with:

```shell
make install
make test
```

By default the tests run against the latest Plone version in the 6.x series.

Documentation is built with:

```shell
make docs
```

## License

The project is licensed under the GPLv2.
