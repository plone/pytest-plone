# Write your first test for a Plone add-on

In this tutorial we will take an add-on that has no pytest tests, and give it one.
By the end you will have a working `conftest.py`, a passing test, and a test that puts content into Plone before it runs.

We assume you have a Plone add-on with `plone.testing` layers — the ones a Plone add-on template gives you — and that its tests currently run, or would run, with `zope.testrunner`.

## Install the plugin

Add `pytest-plone` to your test dependencies and install them.

```shell
pip install pytest-plone
```

## Create the conftest

pytest finds fixtures in a file called `conftest.py`.
Create one at the top of your package, next to your `tests` directory.

We import the testing layers the add-on already has, and hand them to `fixtures_factory`.
It gives us back a dictionary of pytest fixtures, which we drop into the module's namespace.

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

Replace `my.addon` with your own package name.

Notice that we did not write a single fixture ourselves.
The two prefixes, `integration` and `functional`, are the names the generated fixtures will carry.

## Write the test

Create `tests/test_first.py`:

```python
def test_portal_title(portal):
    assert portal.title == "Plone site"
```

Look closely at what is happening here.
There is no class, no `setUp`, and no `self`.
The test asks for a `portal` by naming it as an argument, and pytest builds one and hands it over.

## Run it

```shell
pytest tests/test_first.py
```

You should see one passing test:

```console
tests/test_first.py .                                              [100%]

1 passed
```

The first run takes a few seconds, because Plone has to be set up.
Run it again and notice that it does not get slower — the site is built once and kept for the whole session.

## Ask for content

Real tests need something to test against.
`pytest-plone` can create content for you before the test runs, with a marker.

Add this to `tests/test_first.py`:

```python
import pytest


@pytest.mark.portal(
    content=[{"type": "Document", "id": "doc1", "title": "My first document"}],
)
def test_document_exists(portal):
    assert "doc1" in portal
    assert portal["doc1"].title == "My first document"
```

Run the tests again:

```shell
pytest tests/test_first.py
```

```console
tests/test_first.py ..                                             [100%]

2 passed
```

Both tests pass.
Notice what did *not* happen: the document you created in the second test did not leak into the first one.
Each test runs inside a transaction that is rolled back afterwards, so every test starts from a clean site.

## What you have learned

You have

- turned your existing `plone.testing` layers into pytest fixtures with `fixtures_factory`,
- written a test as a plain function that asks for a `portal`,
- created content with `@pytest.mark.portal` without writing any setup code,
- and seen that tests stay isolated from one another.

That is the whole model.
Everything else `pytest-plone` offers is more fixtures of the same shape.

## Where to go next

- {doc}`/how-to/test-addon-install` — the suite every add-on should have.
- {doc}`/reference/fixtures` — the full catalog of what you can ask for.
- {doc}`/explanation/layers-scopes-and-isolation` — how the isolation you just saw actually works.
