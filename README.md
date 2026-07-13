<h1 align="center">pytest-plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-plone)](https://pypi.org/project/pytest-plone/)
[![PyPI - Status](https://img.shields.io/pypi/status/pytest-plone)](https://pypi.org/project/pytest-plone/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/pytest-plone)](https://pypi.org/project/pytest-plone/)

[![Tests](https://github.com/plone/pytest-plone/actions/workflows/ci.yml/badge.svg)](https://github.com/plone/pytest-plone/actions/workflows/ci.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/plone/pytest-plone)](https://github.com/plone/pytest-plone)
[![GitHub Repo stars](https://img.shields.io/github/stars/plone/pytest-plone?style=social)](https://github.com/plone/pytest-plone)
</div>

**pytest-plone** is a [pytest](https://docs.pytest.org) plugin providing fixtures and helpers to test [Plone](https://plone.org) add-ons.


This package is built on top of [zope.pytestlayer](https://github.com/zopefoundation/zope.pytestlayer).


## Reasoning

Despite the fact Plone, and Zope, have their codebases tested with `unittest`, over the years
`pytest` became the most popular choice for testing in Python.

`pytest` is more flexible and easier to use than `unittest` and has a rich ecosystem of plugins that you can use to extend its functionality.

## Usage

In your top-level `conftest.py` import your testing layers, and also import `fixtures_factory` -- which will accept a iterator of tuples containing the testing layer and a prefix to be used to generate the needed pytest fixtures.

```python
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING
from Products.CMFPlone.testing import PRODUCTS_CMFPLONE_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
            (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
        )
    )
)
```

In the code above, the following pytest fixtures will be available to your tests:

| Fixture | Scope |
| --- | --- |
| functional_session | Session |
| functional_class | Class |
| functional | Function |
| integration_session | Session |
| integration_class | Class |
| integration | Function |

### Session-wide layers

By default `fixtures_factory` registers an autouse session fixture per layer, so each testing layer is set up **once per session**.
This matters for plain function-style tests (`def test_x(portal): ...`): they only depend on the function- and class-scoped fixtures, never on the session fixture, so without this the layer would be torn down and set up again — running a full `applyProfile` — around *every single test*.
Per-test isolation is unaffected: `IntegrationTesting` still rolls back the transaction after each test.

If you need the previous behavior, pass `keep_session=False`:

```python
globals().update(
    fixtures_factory(
        (
            (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
            (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
        ),
        keep_session=False,
    )
)
```


## Fixtures

### generate_mo

|  |  |
| --- | --- |
| Description | Set environment variable to force Zope to compile translation files |
| Required Fixture |  |
| Scope | **Session** |

Add a new fixture to your `conftest.py` to force `generate_mo` to be called for all tests.

```python

@pytest.fixture(scope="session", autouse=True)
def session_initialization(generate_mo):
    """Fixture used to force translation files to be compiled."""
    yield

```

### app

|  |  |
| --- | --- |
| Description | Zope root |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_app(app):
    """Test portal title."""
    assert app.getPhysicalPath() == ("", )

```

### portal

|  |  |
| --- | --- |
| Description | Portal object |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_portal_title(portal):
    """Test portal title."""
    assert portal.title == "Plone Site"

```

### portal_class

|  |  |
| --- | --- |
| Description | Portal object shared across every test method in a class. Honors class-level `@pytest.mark.portal`. |
| Required Fixture | **integration_class** |
| Scope | **Class** |

Class-scoped counterpart to `portal`. Setup runs once per class instead of once per test, so any state created (content, roles, profiles applied) is shared across the class's test methods.

Because the fixture is class-scoped, only `@pytest.mark.portal` decorators applied to the **class** are honored — method-level markers are ignored.

```python
import pytest


@pytest.mark.portal(
    content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
    roles=["Manager"],
)
class TestDocument:
    def test_doc_exists(self, portal_class):
        assert "doc1" in portal_class

    def test_doc_title(self, portal_class):
        assert portal_class["doc1"].title == "Doc"
```

### app_class

|  |  |
| --- | --- |
| Description | Zope root shared across every test method in a class. |
| Required Fixture | **integration_class** |
| Scope | **Class** |

Class-scoped counterpart to `app`. Shares the single per-class setup/teardown of `portal_class` (the app is the portal's container), so a class can request both `app_class` and `portal_class` without setting the layer up twice.

```python
class TestApp:
    def test_app_root(self, app_class):
        assert app_class.getPhysicalPath() == ("",)
```

### http_request

|  |  |
| --- | --- |
| Description | HTTP Request |
| Required Fixture | **integration** |
| Scope | **Function** |


```python
from plone import api


def test_myproduct_controlpanel_view(portal, http_request):
    """Test myproduct_controlpanel browser view is available."""
    view = api.content.get_view(
        "myproduct-controlpanel", portal, http_request
    )
    assert view is not None

```

### functional_app

|  |  |
| --- | --- |
| Description | Zope root bound to the **functional** testing layer. |
| Required Fixture | **functional** |
| Scope | **Function** |

Use this when you need a functional-layer counterpart to `app` — typically for REST API or browser tests.

```python
def test_functional_app(functional_app):
    """Test app title."""
    assert functional_app.getPhysicalPath() == ("", )
```

### functional_portal

|  |  |
| --- | --- |
| Description | Portal object bound to the **functional** testing layer. Honors `@pytest.mark.portal`. |
| Required Fixture | **functional** |
| Scope | **Function** |

Parallel to `portal`, but bound to the functional layer. Accepts the same `@pytest.mark.portal` marker for profiles, content, and roles — see the **Markers** section.

```python
def test_functional_portal_title(functional_portal):
    """Test portal title on the functional layer."""
    assert functional_portal.title == "Plone site"
```

### functional_portal_class

|  |  |
| --- | --- |
| Description | Portal object on the **functional** testing layer, shared across every test method in a class. Honors class-level `@pytest.mark.portal`. |
| Required Fixture | **functional_class** |
| Scope | **Class** |

Class-scoped counterpart to `functional_portal`. The typical use case is a REST API or service test suite that needs a persistent portal across many test methods. As with `portal_class`, only class-level `@pytest.mark.portal` decorators are honored.

```python
import pytest


@pytest.mark.portal(roles=["Manager"])
class TestRESTService:
    def test_portal_available(self, functional_portal_class):
        assert functional_portal_class.title == "Plone site"
```

### functional_app_class

|  |  |
| --- | --- |
| Description | Zope root on the **functional** testing layer, shared across every test method in a class. |
| Required Fixture | **functional_class** |
| Scope | **Class** |

Class-scoped counterpart to `functional_app`. Shares the single per-class setup/teardown of `functional_portal_class`, so a class can request both without setting the layer up twice.

```python
class TestFunctionalApp:
    def test_app_root(self, functional_app_class):
        assert functional_app_class.getPhysicalPath() == ("",)
```

### functional_http_request

|  |  |
| --- | --- |
| Description | HTTP Request bound to the **functional** testing layer. |
| Required Fixture | **functional** |
| Scope | **Function** |

```python
from plone import api


def test_functional_view(functional_portal, functional_http_request):
    """Test a browser view on the functional layer."""
    view = api.content.get_view(
        "myproduct-controlpanel", functional_portal, functional_http_request
    )
    assert view is not None
```

### installer

|  |  |
| --- | --- |
| Description | Installer browser view. Used to install/uninstall/check for an add-on. |
| Required Fixture | **integration** |
| Scope | **Function** |


```python
import pytest


PACKAGE_NAME = "myproduct"


@pytest.fixture
def uninstall(installer):
    """Fixture to uninstall a package."""
    installer.uninstall_product(PACKAGE_NAME)


def test_product_installed(installer):
    """Test if myproduct is installed."""
    assert installer.is_product_installed(PACKAGE_NAME) is True

@pytest.mark.parametrize(
    "package",
    [
        "collective.casestudy",
        "pytest-plone",
    ]
)
def test_dependency_installed(installer, package):
    """Test if dependency is installed."""
    assert installer.is_product_installed(package) is True

```

### uninstalled

|  |  |
| --- | --- |
| Description | Uninstall the add-on under test from the current portal. |
| Required Fixture | **installer**, **package_name** (user-provided) |
| Scope | **Function** |

This fixture removes the duplicate per-project boilerplate from the canonical uninstall smoke test. You must define a `package_name` fixture in your `conftest.py` (or test module) that returns the distribution name of your add-on.

```python
import pytest


@pytest.fixture
def package_name() -> str:
    """Distribution name of the add-on under test."""
    return "collective.person"


class TestSetupUninstall:
    @pytest.fixture(autouse=True)
    def _uninstalled(self, uninstalled):
        """Uninstall the add-on before every test in this class."""

    def test_product_uninstalled(self, installer, package_name):
        assert installer.is_product_installed(package_name) is False
```

### browser_layers

|  |  |
| --- | --- |
| Description | List of available browser layers. Used to test if a specific browser layer is registered. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_browserlayer(browser_layers):
    """Test that IMyProductLayer is registered."""
    from myproduct.interfaces import IMyProductLayer


    assert IMyProductLayer in browser_layers

```

### controlpanel_actions

|  |  |
| --- | --- |
| Description | List of control panel actions ids. Used to test if a specific control panel is installed or not. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_configlet_install(controlpanel_actions):
    """Test if control panel is installed."""
    assert "myproductcontrolpanel" in controlpanel_actions

```

### get_fti

|  |  |
| --- | --- |
| Description | Function to get the Factory Type Info (FTI) for a content type. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_get_fti(get_fti):
    """Test if Document fti is installed."""
    assert get_fti("Document") is not None

```

### get_behaviors

|  |  |
| --- | --- |
| Description | Function to list behaviors for a content type. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
import pytest


def test_block_in_document(get_behaviors):
    """Test if blocks behavior is installed for Document."""
    assert "volto.blocks" in get_behaviors("Document")


@pytest.mark.parametrize(
    "behavior",
    [
        "plone.dublincore",
        "plone.namefromtitle",
        "plone.shortname",
        "plone.excludefromnavigation",
        "plone.relateditems",
        "plone.versioning",
        "volto.blocks",
        "volto.navtitle",
        "volto.preview_image",
        "volto.head_title",
    ],
)
def test_has_behavior(self, get_behaviors, behavior):
    assert behavior in get_behaviors("Document")
```

### get_vocabulary

|  |  |
| --- | --- |
| Description | Function to get a named vocabulary. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
from zope.schema.vocabulary import SimpleVocabulary

VOCAB = "plone.app.vocabularies.AvailableContentLanguages"

def test_get_vocabulary(get_vocabulary):
    """Test plone.app.vocabularies.AvailableContentLanguages."""
    vocab = get_vocabulary(VOCAB)
    assert vocab is not None
    assert isinstance(vocab, SimpleVocabulary)

```

### setup_tool

|  |  |
| --- | --- |
| Description | Portal Setup tool. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
def test_setup_tool(setup_tool):
    """Test setup_tool."""
    assert setup_tool is not None

```

### profile_last_version

|  |  |
| --- | --- |
| Description | Function to get the last version of a profile. |
| Required Fixture | **integration** |
| Scope | **Function** |

```python
PACKAGE_NAME = "collective.case_study"

def test_last_version(profile_last_version):
    """Test setup_tool."""
    profile = f"{PACKAGE_NAME}:default"
    version = profile_last_version(profile)
    assert version == "1000"

```

### apply_profiles

|  |  |
| --- | --- |
| Description | Function to apply GenericSetup profiles to a Plone site. |
| Required Fixture | **integration** |
| Scope | **Session** |

```python
def test_with_profile(portal, apply_profiles):
    """Test that a profile can be applied."""
    apply_profiles(portal, ["my.addon:testing"])
```

### create_content

|  |  |
| --- | --- |
| Description | Function to create content items in a Plone site as the site owner. |
| Required Fixture | **integration** |
| Scope | **Session** |

```python
def test_with_content(portal, create_content):
    """Test that content is created."""
    create_content(portal, [
        {"type": "Document", "id": "doc1", "title": "A Document"},
    ])
    assert "doc1" in portal
```

### grant_roles

|  |  |
| --- | --- |
| Description | Function to grant local roles to the test user on a given context. |
| Required Fixture | **integration** |
| Scope | **Session** |

```python
def test_manager_action(portal, grant_roles):
    """Test an action that requires Manager role."""
    grant_roles(portal, ["Manager"])
    # test user now has Manager role on portal
```

### request_factory

|  |  |
| --- | --- |
| Description | Callable that builds a `RelativeSession` against the functional portal. |
| Required Fixture | **functional_portal** |
| Scope | **Function** |

Replaces the 5+ near-identical request-session fixtures that downstream codebases reimplement. Returns a `RelativeSession` (a thin `requests.Session` subclass that resolves relative URLs against the portal's base URL) with sensible defaults:

- `role="Manager"` — authenticate as the portal owner.
- `role="Anonymous"` (default) — no authentication.
- `basic_auth=(user, password)` — any other identity; takes precedence over `role`.
- `api=True` (default) — suffix the base URL with `++api++` so relative calls hit the REST API.

Sessions are closed automatically at the end of the test.

```python
def test_list_content(request_factory):
    """Test that the Manager role can list content."""
    session = request_factory(role="Manager")
    response = session.get("/")
    assert response.status_code == 200
```

### manager_request

|  |  |
| --- | --- |
| Description | `RelativeSession` pre-authenticated as the portal owner (Manager). |
| Required Fixture | **request_factory** |
| Scope | **Function** |

```python
def test_controlpanels(manager_request):
    """Test listing of control panels."""
    response = manager_request.get("/@controlpanels")
    assert response.status_code == 200
```

### anon_request

|  |  |
| --- | --- |
| Description | `RelativeSession` with no authentication (Anonymous). |
| Required Fixture | **request_factory** |
| Scope | **Function** |

```python
def test_public_endpoint(anon_request):
    """Test a public REST API endpoint."""
    response = anon_request.get("/")
    assert response.status_code == 200
```

## Markers

### @pytest.mark.portal

Configure the `portal` fixture with GenericSetup profiles, pre-created content, and/or user roles — without overriding the fixture.

| Parameter | Type | Description |
| --- | --- | --- |
| `profiles` | `list[str]` | GenericSetup profile IDs to apply (e.g. `["my.addon:testing"]`) |
| `content` | `list[dict]` | Dicts passed as keyword arguments to `plone.api.content.create` |
| `roles` | `list[str]` | Roles granted to the test user via `plone.api.user.grant_roles` |

Setup is applied in order: **profiles → content → roles**.

```python
import pytest


@pytest.mark.portal(
    profiles=["my.addon:testing"],
    content=[{"type": "Document", "id": "doc1", "title": "Doc 1"}],
    roles=["Manager"],
)
def test_something(portal):
    """Test with custom portal setup."""
    assert "doc1" in portal
```

Tests without the marker see no behavior change — fully backwards-compatible.

#### Content specifications

Each dict in `content` is passed as keyword arguments to `plone.api.content.create`. Two keys receive special handling and are consumed before the call:

| Key | Description |
| --- | --- |
| `_container` | Path to the container the item is created in, relative to the site root (e.g. `"/folder"`). Defaults to the portal when absent. |
| `_review_state` | Target workflow state; the item is transitioned there after creation via `plone.api.content.transition`. |

Items are created in list order, so a container listed earlier can be referenced by a later item's `_container`:

```python
import pytest


@pytest.mark.portal(
    content=[
        {"type": "Folder", "id": "folder", "title": "Folder"},
        {
            "type": "Document",
            "id": "doc1",
            "title": "Nested & published",
            "_container": "/folder",
            "_review_state": "published",
        },
    ],
)
def test_nested_content(portal):
    """The document lives in the folder and is published."""
    from plone import api

    doc = portal["folder"]["doc1"]
    assert api.content.get_state(obj=doc) == "published"
```

## Plugin Development

You need a working `python` environment (system, virtualenv, pyenv, etc) version 3.8 or superior.

Then install the dependencies and a development instance using:

```bash
make install
```

To run tests for this package:

```bash
make test
```

By default we use the latest Plone version in the 6.x series.

## License

The project is licensed under the GPLv2.
