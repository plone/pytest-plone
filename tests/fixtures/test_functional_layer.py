"""Tests for functional-layer fixtures."""

import pytest


@pytest.mark.no_cover
class TestFunctionalFixtures:
    """``functional_app``, ``functional_portal`` and ``functional_http_request``."""

    def test_functional_app(self, testdir):
        testdir.makepyfile(
            """
            def test_functional_app(functional_app):
                assert functional_app.getPhysicalPath() == ("",)
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_functional_portal(self, testdir):
        testdir.makepyfile(
            """
            def test_functional_portal(functional_portal):
                assert functional_portal.title == "Plone site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_functional_http_request(self, testdir):
        testdir.makepyfile(
            """
            def test_functional_http_request(functional_http_request):
                assert functional_http_request.method == "GET"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestFunctionalPortalMarker:
    """``functional_portal`` honors ``@pytest.mark.portal`` like ``portal``."""

    def test_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager"])
            def test_user_has_manager_role(functional_portal):
                roles = api.user.get_roles(
                    username=TEST_USER_ID, obj=functional_portal
                )
                assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_content(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "A Document"}],
            )
            def test_document_exists(functional_portal):
                assert "doc1" in functional_portal
                assert functional_portal["doc1"].title == "A Document"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_no_marker(self, testdir):
        testdir.makepyfile(
            """
            def test_functional_portal_no_marker(functional_portal):
                assert functional_portal.title == "Plone site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestFunctionalPortalMarkerIsolation:
    """Marker changes don't leak between functional-layer tests."""

    def test_content_does_not_leak(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
            )
            def test_first(functional_portal):
                assert "doc1" in functional_portal

            def test_second(functional_portal):
                assert "doc1" not in functional_portal
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)

    def test_roles_do_not_leak(self, testdir):
        # "Reviewer" (not the baseline "Manager") so presence in the second test
        # is a real leak — see the equivalent integration test for the rationale.
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Reviewer"])
            def test_first(functional_portal):
                roles = api.user.get_roles(
                    username=TEST_USER_ID, obj=functional_portal
                )
                assert "Reviewer" in roles

            def test_second(functional_portal):
                roles = api.user.get_roles(
                    username=TEST_USER_ID, obj=functional_portal
                )
                assert "Reviewer" not in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)
