"""Base fixtures."""

from .markers import apply_portal_marker
from collections.abc import Generator
from OFS.Application import Application
from plone.testing.layer import Layer
from Products.CMFPlone.Portal import PloneSite
from ZPublisher.HTTPRequest import HTTPRequest

import pytest


@pytest.fixture()
def app(integration: Layer) -> Application:
    """Returns the root of a Zope application for an integration Layer.

    Example usage:
    ```python
    def test_app(self, app):
        assert app.title == "Zope"
    ```
    """
    return integration["app"]


@pytest.fixture()
def portal(integration: Layer, request: pytest.FixtureRequest) -> PloneSite:
    """Returns the default Plone Site for an integration Layer.

    Supports ``@pytest.mark.portal`` to apply GenericSetup profiles,
    create content, and grant roles before the test runs.

    Example usage:
    ```python
    def test_portal(self, portal):
        assert portal.title == "Plone site"

    @pytest.mark.portal(
        profiles=["my.addon:testing"],
        content=[{"type": "Document", "id": "doc1", "title": "A document"}],
        roles=["Manager"],
    )
    def test_portal_with_marker(self, portal):
        assert "doc1" in portal
    ```
    """
    portal: PloneSite = integration["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture(scope="class")
def app_class(
    integration_class: Layer,
) -> Generator[Application, None, None]:
    """Returns the root of a Zope application for an integration Layer, class-scoped.

    Class-scoped counterpart to :func:`app`. ``zope.pytestlayer`` only invokes
    ``testSetUp`` for function-scoped fixtures, so this fixture drives the
    per-class ``testSetUp``/``testTearDown`` lifecycle itself. :func:`portal_class`
    builds on it, so a test class can request both ``app_class`` and
    ``portal_class`` without setting the layer up twice.

    Example usage:
    ```python
    class TestApp:
        def test_app(self, app_class):
            assert app_class.title == "Zope"
    ```
    """
    integration_class.testSetUp()
    try:
        yield integration_class["app"]
    finally:
        integration_class.testTearDown()


@pytest.fixture(scope="class")
def portal_class(
    app_class: Application,
    integration_class: Layer,
    request: pytest.FixtureRequest,
) -> PloneSite:
    """Returns the default Plone Site for an integration Layer, class-scoped.

    Class-scoped counterpart to :func:`portal`. The same portal instance is
    shared across every test method in the class, so setup runs once per class
    instead of once per test. The per-class ``testSetUp``/``testTearDown``
    lifecycle is driven by :func:`app_class`, on which this fixture depends.

    Honors ``@pytest.mark.portal`` **applied at the class level** — method-level
    markers are not visible to a class-scoped fixture and are ignored.

    Example usage:
    ```python
    @pytest.mark.portal(
        content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
        roles=["Manager"],
    )
    class TestSomething:
        def test_one(self, portal_class):
            assert "doc1" in portal_class

        def test_two(self, portal_class):
            assert "doc1" in portal_class
    ```
    """
    portal: PloneSite = integration_class["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture
def http_request(integration: Layer) -> HTTPRequest:
    """Returns the current request object.

    Example usage:
    ```python
    def test_request(self, request):
        assert request.method == "GET"
    ```
    """
    return integration["request"]


@pytest.fixture()
def functional_app(functional: Layer) -> Application:
    """Returns the root of a Zope application for a functional Layer.

    Mirrors :func:`app` but bound to the ``functional`` layer. Use this in
    REST API, browser, or other tests that require transaction-level
    isolation instead of the integration-layer stacked-DemoStorage.

    Example usage:
    ```python
    def test_functional_app(self, functional_app):
        assert functional_app.title == "Zope"
    ```
    """
    return functional["app"]


@pytest.fixture()
def functional_portal(functional: Layer, request: pytest.FixtureRequest) -> PloneSite:
    """Returns the default Plone Site for a functional Layer.

    Mirrors :func:`portal` but bound to the ``functional`` layer and also
    honors ``@pytest.mark.portal`` for GenericSetup profiles, pre-created
    content, and test-user roles.

    Example usage:
    ```python
    def test_functional_portal(self, functional_portal):
        assert functional_portal.title == "Plone site"
    ```
    """
    portal: PloneSite = functional["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture(scope="class")
def functional_app_class(
    functional_class: Layer,
) -> Generator[Application, None, None]:
    """Returns the root of a Zope application for a functional Layer, class-scoped.

    Class-scoped counterpart to :func:`functional_app`. ``zope.pytestlayer`` only
    invokes ``testSetUp`` for function-scoped fixtures, so this fixture drives the
    per-class ``testSetUp``/``testTearDown`` lifecycle itself.
    :func:`functional_portal_class` builds on it, so a test class can request both
    without setting the layer up twice.

    Example usage:
    ```python
    class TestFunctionalApp:
        def test_app(self, functional_app_class):
            assert functional_app_class.title == "Zope"
    ```
    """
    functional_class.testSetUp()
    try:
        yield functional_class["app"]
    finally:
        functional_class.testTearDown()


@pytest.fixture(scope="class")
def functional_portal_class(
    functional_app_class: Application,
    functional_class: Layer,
    request: pytest.FixtureRequest,
) -> PloneSite:
    """Returns the default Plone Site for a functional Layer, class-scoped.

    Class-scoped counterpart to :func:`functional_portal`. The same portal
    instance is shared across every test method in the class — the typical
    pattern for REST API / service test suites that need a persistent portal.
    The per-class ``testSetUp``/``testTearDown`` lifecycle is driven by
    :func:`functional_app_class`, on which this fixture depends.

    Honors ``@pytest.mark.portal`` **applied at the class level** — method-level
    markers are not visible to a class-scoped fixture and are ignored.

    Example usage:
    ```python
    @pytest.mark.portal(roles=["Manager"])
    class TestRESTService:
        def test_one(self, functional_portal_class):
            assert functional_portal_class.title == "Plone site"

        def test_two(self, functional_portal_class):
            ...
    ```
    """
    portal: PloneSite = functional_class["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture
def functional_http_request(functional: Layer) -> HTTPRequest:
    """Returns the current request object for a functional Layer.

    Mirrors :func:`http_request` but bound to the ``functional`` layer.

    Example usage:
    ```python
    def test_functional_request(self, functional_http_request):
        assert functional_http_request.method == "GET"
    ```
    """
    return functional["request"]
