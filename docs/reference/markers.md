---
myst:
  html_meta:
    "description": "The pytest.mark.portal marker configures the portal fixture with profiles, content, and roles."
    "property=og:description": "The pytest.mark.portal marker configures the portal fixture with profiles, content, and roles."
    "property=og:title": "pytest-plone markers"
    "keywords": "Plone, pytest, marker, portal, profiles, roles"
---

# Markers

## `@pytest.mark.portal`

Configures a portal fixture before the test runs.

The marker is honored by all four [portal fixtures](fixtures.md#portal-and-app): `portal`, `portal_class`, `functional_portal`, and `functional_portal_class`.

It accepts three keyword arguments, all optional:

`profiles`
:   A list of GenericSetup profile identifiers to apply.
    Both `"my.addon:default"` and the full `"profile-my.addon:default"` form work—the `profile-` prefix is added when missing.
    Profiles are applied as the site owner, like `plone.app.testing.applyProfile`, so an import step that creates content works whatever the test user's roles.

`content`
:   A list of dictionaries.
    Each is passed as keyword arguments to `plone.api.content.create(container=portal, **spec)`.
    Content is created as the site owner.

`roles`
:   A list of roles to grant to the default test user on the portal.

They are applied in that order: profiles, then content, then roles.
Because roles are granted last, `roles` has no effect on how profiles are applied or content is created; both already run as the site owner.
After the marker runs, the test body runs as the test user, with only the roles it had plus those in `roles`.

Content created by `content`, or by the import steps of `profiles`, is fully indexed before the test body runs.
The marker flushes the catalog's indexing queue, which otherwise waits for a transaction boundary that never comes inside a test.
This matters for reads that go straight to an index, such as `portal_catalog.uniqueValuesFor()` and the vocabularies built on it; catalog queries flush the queue on their own.

```python
import pytest


@pytest.mark.portal(
    profiles=["my.addon:testing"],
    content=[{"type": "Document", "id": "doc1", "title": "A document"}],
    roles=["Manager"],
)
def test_portal_with_marker(portal):
    assert "doc1" in portal
```

```{important}
On the class-scoped fixtures, only a marker applied to the **class** is honored.
A class-scoped fixture is created once for the whole class and cannot see markers on individual methods, so a method-level marker is silently ignored.
```

```python
import pytest


@pytest.mark.portal(roles=["Manager"])
class TestDocument:
    def test_one(self, portal_class):
        assert portal_class.title == "Plone site"

    def test_two(self, portal_class):
        assert portal_class.title == "Plone site"
```

## Registering the marker

`pytest-plone` registers `portal` with pytest itself, so you do not need to declare it in your `pytest.ini` or `pyproject.toml`.
