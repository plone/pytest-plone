"""Fixtures used to test vocabularies."""

from pytest_plone import _types as t
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import pytest


@pytest.fixture(scope="session")
def get_vocabulary() -> t.VocabularyGetter:
    """Provides a method to get a named vocabulary in a given context.

    Example usage:
    ```python
    def test_vocabulary(portal, get_vocabulary):
        voc = get_vocabulary("plone.app.vocabularies.SupportedContentLanguages", portal)
        assert "en" in voc
        term = voc.getTerm("en")
        assert term.title == "English"
    ```
    """

    def get_vocabulary(name: str, context: t.Context) -> t.PloneVocabulary:
        """Get a named vocabulary in a given context."""
        return getUtility(IVocabularyFactory, name)(context)

    return get_vocabulary
