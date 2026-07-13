# How to set up pytest-plone in your add-on

This guide shows you how to add `pytest-plone` to an existing Plone add-on.

## Before you start

You need testing layers.

A testing layer is the object that builds a Plone site for your tests: it loads your ZCML, installs your GenericSetup profile, and hands the result to each test.
By convention you declare yours in a `testing.py` module in your package, building on the fixtures `plone.app.testing` provides.

`pytest-plone` does not replace any of this.
It takes the layers you already have and turns them into pytest fixtures.
If your add-on has no `testing.py` yet, write one first — the packages that own the layer machinery document how:

```{seealso}
- [plone.app.testing](https://github.com/plone/plone.app.testing/blob/master/README.rst) — the Plone-specific layers and fixtures, and how to write your own `testing.py`.
- [plone.testing](https://github.com/plone/plone.testing/blob/master/src/plone/testing/README.rst) — the underlying layer model.
```

## Install the package

Add `pytest-plone` to your test dependencies:

```toml
[project.optional-dependencies]
test = [
    "pytest-plone",
    "plone.app.testing",
]
```

## Write the conftest

In your top-level `conftest.py`, import your testing layers and pass them to `fixtures_factory` together with a prefix for each.
Inject the result into the module namespace so pytest discovers the fixtures.

```python
from my.addon.testing import MY_ADDON_FUNCTIONAL_TESTING
from my.addon.testing import MY_ADDON_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (MY_ADDON_FUNCTIONAL_TESTING, "functional"),
            (MY_ADDON_INTEGRATION_TESTING, "integration"),
        )
    )
)
```

The prefixes name the generated fixtures.
With `integration` and `functional` you get `integration`, `integration_class`, `integration_session`, and the three `functional` counterparts.
Stick to these two names unless you have a reason not to — the fixtures in {doc}`/reference/fixtures` are built on them.

## Write a test

Ask for what you need by naming it.

```python
def test_portal_title(portal):
    assert portal.title == "Plone site"
```

## Run the suite

```shell
pytest
```

## Declare your package name

Several add-on fixtures need to know which distribution is under test.
Provide a `package_name` fixture in your `conftest.py`:

```python
import pytest


@pytest.fixture
def package_name() -> str:
    return "my.addon"
```

This unlocks [`uninstalled`](/reference/fixtures.md#add-ons), which removes the boilerplate from the canonical uninstall test.

## Where to go next

- {doc}`test-addon-install` — the canonical install and uninstall suite.
- {doc}`speed-up-the-test-suite` — if the suite feels slower than it should.
- {doc}`/reference/fixtures` — everything you can ask for.
