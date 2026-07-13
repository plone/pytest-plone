"""Fixtures used in content tests."""

from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import _types as t
from pytest_plone.fixtures import markers
from zope.component import queryUtility

import pytest


@pytest.fixture()
def get_fti(portal: PloneSite) -> t.FTIGetter:
    """Provides a method to get the Factory Type Information for a type by name.

    Example usage:
    ```python
    def test_fti(get_fti):
        fti = get_fti("Person")
        assert IDexterityFTI.providedBy(fti)
        assert fti.title == "Person"
    ```
    """

    def get_fti(name: str) -> DexterityFTI:
        """Get the Factory Type Information for a type by name."""
        return queryUtility(IDexterityFTI, name=name)

    return get_fti


@pytest.fixture()
def get_behaviors(get_fti: t.FTIGetter) -> t.BehaviorsGetter:
    """Provides a method to get the list of behaviors for a type.

    Example usage:
    ```python
    def test_behaviors(get_behaviors):
        behaviors = get_behaviors("Person")
        assert "plone.namefromtitle" in behaviors
    ```
    """

    def get_behaviors(name: str) -> list[str]:
        """Get the list of behaviors for a content type."""
        fti = get_fti(name)
        return list(fti.behaviors)

    return get_behaviors


@pytest.fixture(scope="session")
def create_content() -> t.ContentCreator:
    """Create content items in a Plone site as the site owner.

    Example usage:
    ```python
    def test_with_content(portal, create_content):
        create_content(portal, [
            {"type": "Document", "id": "doc1", "title": "A Document"},
        ])
        assert "doc1" in portal
    ```
    """

    def func(container: PortalContent, content: list[dict]) -> None:
        markers.create_content(container, content)

    return func
