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
    def test_app(app):
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
    def test_portal(portal):
        assert portal.title == "Plone site"

    @pytest.mark.portal(
        profiles=["my.addon:testing"],
        content=[{"type": "Document", "id": "doc1", "title": "A document"}],
        roles=["Manager"],
    )
    def test_portal_with_marker(portal):
        assert "doc1" in portal
    ```
    """
    portal: PloneSite = integration["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture(scope="class")
def portal_class(
    integration_class: Layer, request: pytest.FixtureRequest
) -> Generator[PloneSite, None, None]:
    """Returns the default Plone Site for an integration Layer, class-scoped.

    Class-scoped counterpart to :func:`portal`. The same portal instance is
    shared across every test method in the class, so setup runs once per class
    instead of once per test.

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
    # ``zope.pytestlayer`` only invokes ``testSetUp`` for function-scoped
    # fixtures, so the layer's ``portal`` key is unset at class scope. Drive
    # the per-test lifecycle ourselves so the same portal/transaction spans
    # every test method in the class.
    integration_class.testSetUp()
    try:
        portal: PloneSite = integration_class["portal"]
        apply_portal_marker(portal, request)
        yield portal
    finally:
        integration_class.testTearDown()


@pytest.fixture
def http_request(integration: Layer) -> HTTPRequest:
    """Returns the current request object.

    Example usage:
    ```python
    def test_http_request(http_request):
        assert http_request.method == "GET"
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
    def test_functional_app(functional_app):
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
    def test_functional_portal(functional_portal):
        assert functional_portal.title == "Plone site"
    ```
    """
    portal: PloneSite = functional["portal"]
    apply_portal_marker(portal, request)
    return portal


@pytest.fixture(scope="class")
def functional_portal_class(
    functional_class: Layer, request: pytest.FixtureRequest
) -> Generator[PloneSite, None, None]:
    """Returns the default Plone Site for a functional Layer, class-scoped.

    Class-scoped counterpart to :func:`functional_portal`. The same portal
    instance is shared across every test method in the class — the typical
    pattern for REST API / service test suites that need a persistent portal.

    Honors ``@pytest.mark.portal`` **applied at the class level** — method-level
    markers are not visible to a class-scoped fixture and are ignored.

    Example usage:
    ```python
    @pytest.mark.portal(roles=["Manager"])
    class TestRESTService:
        def test_one(self, functional_portal_class):
            assert functional_portal_class.title == "Plone site"

        def test_two(self, functional_portal_class):
            assert "plone" in functional_portal_class.absolute_url()
    ```
    """
    functional_class.testSetUp()
    try:
        portal: PloneSite = functional_class["portal"]
        apply_portal_marker(portal, request)
        yield portal
    finally:
        functional_class.testTearDown()


@pytest.fixture
def functional_http_request(functional: Layer) -> HTTPRequest:
    """Returns the current request object for a functional Layer.

    Mirrors :func:`http_request` but bound to the ``functional`` layer.

    Example usage:
    ```python
    def test_functional_http_request(functional_http_request):
        assert functional_http_request.method == "GET"
    ```
    """
    return functional["request"]
