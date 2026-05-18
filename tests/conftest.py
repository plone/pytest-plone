from _pytest.pytester import Pytester
from _pytest.python import Metafunc

import pytest


pytest_plugins = ["pytester"]


@pytest.fixture
def testdir(pytester: Pytester) -> Pytester:
    # create a temporary conftest.py file
    pytester.makeconftest(
        """
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

        """
    )
    return pytester


OUR_FIXTURES = [
    "anon_request",
    "app",
    "apply_profiles",
    "browser_layers",
    "controlpanel_actions",
    "create_content",
    "functional_app",
    "functional_http_request",
    "functional_portal",
    "functional_portal_class",
    "generate_mo",
    "get_behaviors",
    "get_fti",
    "get_vocabulary",
    "grant_roles",
    "http_request",
    "installer",
    "manager_request",
    "portal",
    "portal_class",
    "profile_last_version",
    "request_factory",
    "setup_tool",
]


def pytest_generate_tests(metafunc: Metafunc):
    """Parametrize tests generation."""
    if "fixture_name" in metafunc.fixturenames:
        metafunc.parametrize("fixture_name", OUR_FIXTURES)
