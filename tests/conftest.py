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


@pytest.fixture
def testdir_no_keep(pytester: Pytester) -> Pytester:
    # Like ``testdir`` but opts out of the session-wide layer keep.
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
                ),
                keep_session=False,
            )
        )

        """
    )
    return pytester


OUR_FIXTURES = [
    "anon_request",
    "answers",
    "app",
    "app_class",
    "apply_profiles",
    "browser_layers",
    "controlpanel_actions",
    "create_content",
    "create_site",
    "distribution_name",
    "functional_app",
    "functional_app_class",
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
    "site_logo",
    "site_owner_name",
    "site_owner_password",
]


def pytest_generate_tests(metafunc: Metafunc):
    """Parametrize tests generation."""
    if "fixture_name" in metafunc.fixturenames:
        metafunc.parametrize("fixture_name", OUR_FIXTURES)
