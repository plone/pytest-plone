"""Tests for class-scoped portal fixtures."""

import pytest


@pytest.mark.no_cover
class TestPortalClass:
    """``portal_class`` is class-scoped and shared across test methods."""

    def test_portal_class_returns_portal(self, testdir):
        testdir.makepyfile(
            """
            class TestPortalClassBasic:
                def test_portal_title(self, portal_class):
                    assert portal_class.title == "Plone site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_portal_class_shared_across_methods(self, testdir):
        """Mutations from one test method are visible to the next."""
        testdir.makepyfile(
            """
            from plone import api
            from plone.app.testing import SITE_OWNER_NAME

            class TestPortalClassShared:
                def test_a_create(self, portal_class):
                    with api.env.adopt_user(SITE_OWNER_NAME):
                        api.content.create(
                            container=portal_class,
                            type="Document",
                            id="shared-doc",
                            title="Shared",
                        )
                    assert "shared-doc" in portal_class

                def test_b_visible(self, portal_class):
                    assert "shared-doc" in portal_class
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)


@pytest.mark.no_cover
class TestPortalClassMarker:
    """``portal_class`` honors ``@pytest.mark.portal`` at the class level."""

    def test_class_level_content(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
            )
            class TestPortalClassContent:
                def test_doc_exists(self, portal_class):
                    assert "doc1" in portal_class

                def test_doc_still_there(self, portal_class):
                    assert "doc1" in portal_class
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)

    def test_class_level_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager"])
            class TestPortalClassRoles:
                def test_manager_role(self, portal_class):
                    roles = api.user.get_roles(
                        username=TEST_USER_ID, obj=portal_class
                    )
                    assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestAppClass:
    """``app_class`` is the class-scoped Zope app root."""

    def test_app_class_returns_app(self, testdir):
        testdir.makepyfile(
            """
            class TestAppClassBasic:
                def test_app_title(self, app_class):
                    assert app_class.title == "Zope"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_app_class_and_portal_class_share_lifecycle(self, testdir):
        """Requesting both must not set the layer up twice."""
        testdir.makepyfile(
            """
            from Acquisition import aq_base

            class TestAppAndPortal:
                def test_app_is_portal_parent(self, app_class, portal_class):
                    assert aq_base(app_class) is aq_base(portal_class.aq_parent)
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestFunctionalPortalClass:
    """``functional_portal_class`` is class-scoped on the functional layer."""

    def test_functional_portal_class_returns_portal(self, testdir):
        testdir.makepyfile(
            """
            class TestFunctionalPortalClassBasic:
                def test_portal_title(self, functional_portal_class):
                    assert functional_portal_class.title == "Plone site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_class_level_marker_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager"])
            class TestFunctionalPortalClassRoles:
                def test_manager_role(self, functional_portal_class):
                    roles = api.user.get_roles(
                        username=TEST_USER_ID, obj=functional_portal_class
                    )
                    assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestFunctionalAppClass:
    """``functional_app_class`` is the class-scoped Zope app root."""

    def test_functional_app_class_returns_app(self, testdir):
        testdir.makepyfile(
            """
            class TestFunctionalAppClassBasic:
                def test_app_title(self, functional_app_class):
                    assert functional_app_class.title == "Zope"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)
