"""Tests for plone.distribution fixtures."""

import pytest


# A conftest whose layer comes from ``plone.distribution.testing``: it registers
# the ``testing`` distribution (loading its ZCML and the products it needs) and
# creates a base site. ``create_site`` then builds a second site from the same
# distribution. Requires ``plone.app.caching`` and ``plone.volto`` (test deps).
DISTRIBUTION_CONFTEST = """
    from plone.distribution.testing import INTEGRATION_TESTING
    from pytest_plone import fixtures_factory

    pytest_plugins = ["pytest_plone"]

    globals().update(fixtures_factory(((INTEGRATION_TESTING, "integration"),)))
"""


@pytest.mark.no_cover
class TestDistributionDefaults:
    """Default values of the plone.distribution helper fixtures."""

    def test_distribution_name(self, testdir):
        testdir.makepyfile(
            """
            def test_name(distribution_name):
                assert distribution_name == "testing"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_answers(self, testdir):
        testdir.makepyfile(
            """
            def test_default_answers(answers):
                assert answers["site_id"] == "plone-site"
                assert answers["setup_content"] is False
                assert answers["site_logo"]
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_site_owner_fixtures(self, testdir):
        testdir.makepyfile(
            """
            from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

            def test_owner(site_owner_name, site_owner_password):
                assert site_owner_name == SITE_OWNER_NAME
                assert site_owner_password == SITE_OWNER_PASSWORD
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestCreateSite:
    """``create_site`` creates a Plone site from a distribution."""

    def test_create_site(self, testdir):
        testdir.makeconftest(DISTRIBUTION_CONFTEST)
        testdir.makepyfile(
            """
            from plone import api

            def test_site_created(create_site, app, answers):
                site = create_site(app, answers)
                assert site.getId() == "plone-site"
                assert site.title == "Plone Site"
                # Set as the current local site
                assert api.portal.get() is site
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_create_site_is_idempotent(self, testdir):
        testdir.makeconftest(DISTRIBUTION_CONFTEST)
        testdir.makepyfile(
            """
            def test_recreate(create_site, app, answers):
                first = create_site(app, answers)
                assert "plone-site" in app.objectIds()
                # Calling again deletes the existing site and recreates it
                second = create_site(app, answers)
                assert app.objectIds().count("plone-site") == 1
                assert second.getId() == "plone-site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)
