---
myst:
  html_meta:
    "description": "Every fixture provided by pytest-plone, with its scope and requirements."
    "property=og:description": "Every fixture provided by pytest-plone, with its scope and requirements."
    "property=og:title": "pytest-plone fixtures"
    "keywords": "Plone, pytest, fixtures, portal, integration, functional"
---

# Fixtures

Every fixture `pytest-plone` registers, grouped by what it gives you.

The `integration` and `functional` fixtures these depend on are generated from your testing layers by {doc}`fixtures_factory <api>`.
For what the two layers mean and when to choose which, see {doc}`/explanation/layers-scopes-and-isolation`.

## Overview

| Fixture | Scope | Requires |
| --- | --- | --- |
| `app` | Function | `integration` |
| `portal` | Function | `integration` |
| `portal_class` | Class | `integration_class` |
| `http_request` | Function | `integration` |
| `functional_app` | Function | `functional` |
| `functional_portal` | Function | `functional` |
| `functional_portal_class` | Class | `functional_class` |
| `functional_http_request` | Function | `functional` |
| `request_factory` | Function | `functional_portal` |
| `manager_request` | Function | `request_factory` |
| `anon_request` | Function | `request_factory` |
| `installer` | Function | `portal` |
| `uninstalled` | Function | `installer`, `package_name` |
| `browser_layers` | Function | `portal` |
| `controlpanel_actions` | Function | `portal` |
| `setup_tool` | Function | `portal` |
| `profile_last_version` | Function | `setup_tool` |
| `apply_profiles` | Session |—|
| `get_fti` | Function | `portal` |
| `get_behaviors` | Function | `get_fti` |
| `create_content` | Session |—|
| `grant_roles` | Session |—|
| `get_vocabulary` | Session |—|
| `generate_mo` | Session |—|

## Portal and app

The Plone site and the Zope root, on either testing layer.

The `functional_` variants are bound to the functional layer, which uses a real transaction and a running server rather than the integration layer's stacked `DemoStorage`.
Use them for REST API and browser tests.

The class-scoped variants share one portal across every test method in a class.
They honor `@pytest.mark.portal` only when it is applied to the **class**; a class-scoped fixture cannot see method-level markers.

```{autodoc2-object} pytest_plone.fixtures.base.app
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.portal
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.portal_class
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.functional_app
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.functional_portal
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.functional_portal_class
render_plugin = "myst"
```

## Requests

`http_request` and `functional_http_request` return the request object bound to the layer.

`request_factory` is different in kind: it builds authenticated HTTP sessions that talk to a running Plone over the network, which is what REST API tests need.
`manager_request` and `anon_request` are shorthands for the two common identities.

```{autodoc2-object} pytest_plone.fixtures.base.http_request
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.functional_http_request
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.requests.request_factory
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.requests.manager_request
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.requests.anon_request
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.requests.RelativeSession
render_plugin = "myst"
```

## Add-ons

Fixtures for the canonical add-on test suite: is the product installed, are its browser layers registered, is its control panel there, is its profile at the expected version.

```{autodoc2-object} pytest_plone.fixtures.addons.installer
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.addons.uninstalled
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.addons.browser_layers
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.addons.controlpanel_actions
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.addons.setup_tool
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.addons.profile_last_version
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.addons.apply_profiles
render_plugin = "myst"
```

## Content

Inspect content types and create content items.

`create_content` is session-scoped and takes the container explicitly, so you can call it against any portal or folder.

```{autodoc2-object} pytest_plone.fixtures.content.get_fti
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.content.get_behaviors
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.content.create_content
render_plugin = "myst"
```

## Security

```{autodoc2-object} pytest_plone.fixtures.security.grant_roles
render_plugin = "myst"
```

## Vocabularies

```{autodoc2-object} pytest_plone.fixtures.vocabularies.get_vocabulary
render_plugin = "myst"
```

## Environment

```{autodoc2-object} pytest_plone.fixtures.env.generate_mo
render_plugin = "myst"
```

`generate_mo` does nothing unless a test requests it.
To compile translations once for the whole suite, pull it in from an autouse session fixture in your `conftest.py`:

```python
import pytest


@pytest.fixture(scope="session", autouse=True)
def session_initialization(generate_mo):
    """Force translation files to be compiled."""
```
