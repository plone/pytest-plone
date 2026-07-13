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
| `app_class` | Class | `integration_class` |
| `portal_class` | Class | `integration_class` |
| `http_request` | Function | `integration` |
| `functional_app` | Function | `functional` |
| `functional_portal` | Function | `functional` |
| `functional_app_class` | Class | `functional_class` |
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
| `create_site` | Session | `distribution_name`, `site_owner_name` |
| `distribution_name` | Session |—|
| `answers` | Session | `site_logo` |
| `site_logo` | Session |—|
| `site_owner_name` | Session |—|
| `site_owner_password` | Session |—|
| `generate_mo` | Session |—|

## Portal and app

The Plone site and the Zope root, on either testing layer.

The `functional_` variants are bound to the functional layer, which uses a real transaction and a running server rather than the integration layer's stacked `DemoStorage`.
Use them for REST API and browser tests.

The class-scoped variants share one portal across every test method in a class.
They honor `@pytest.mark.portal` only when it is applied to the **class**; a class-scoped fixture cannot see method-level markers.

The `app_class` and `functional_app_class` fixtures return the Zope root at class scope.
Each one drives the single per-class setup and teardown that its portal counterpart depends on, so a class can ask for both the app and the portal without setting the layer up twice.

```{autodoc2-object} pytest_plone.fixtures.base.app
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.portal
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.app_class
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

```{autodoc2-object} pytest_plone.fixtures.base.functional_app_class
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

## Distribution

Create a Plone site from a `plone.distribution` distribution, the way a real deployment does.

`create_site` returns a callable that builds a **new** site in a Zope app from the distribution named by `distribution_name`, using the answers from `answers`, and sets it as the current site.
It first deletes any existing site with the same id, so each call starts from a clean state.
The distribution named by `distribution_name` must be registered, for example by loading the ZCML of a package that declares it with a `plone:distribution` directive.

The `distribution_name`, `answers`, and `site_logo` fixtures are meant to be **overridden** in your own `conftest.py` to point at your distribution and customize the site.
`site_owner_name` and `site_owner_password` expose the site owner credentials, so tests and fixtures can depend on them instead of importing the constants.

```{autodoc2-object} pytest_plone.fixtures.distribution.create_site
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.distribution.distribution_name
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.distribution.answers
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.distribution.site_logo
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.site_owner_name
render_plugin = "myst"
```

```{autodoc2-object} pytest_plone.fixtures.base.site_owner_password
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
