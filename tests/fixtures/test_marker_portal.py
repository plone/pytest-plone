"""Tests for @pytest.mark.portal marker support."""

import pytest


@pytest.mark.no_cover
class TestPortalMarkerNoArgs:
    """Portal fixture works without the marker (backwards-compatible)."""

    def test_portal_without_marker(self, testdir):
        testdir.makepyfile(
            """
            def test_portal_no_marker(portal):
                assert portal.title == "Plone site"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerRoles:
    """Portal marker applies roles to the test user."""

    def test_grant_manager_role(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager"])
            def test_user_has_manager_role(portal):
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_grant_multiple_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Manager", "Reviewer"])
            def test_user_has_multiple_roles(portal):
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Manager" in roles
                assert "Reviewer" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerContent:
    """Portal marker creates content in the portal."""

    def test_create_document(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "A Document"}],
            )
            def test_document_exists(portal):
                assert "doc1" in portal
                assert portal["doc1"].title == "A Document"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_create_multiple_content(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[
                    {"type": "Document", "id": "doc1", "title": "Doc 1"},
                    {"type": "Document", "id": "doc2", "title": "Doc 2"},
                ],
            )
            def test_multiple_content(portal):
                assert "doc1" in portal
                assert "doc2" in portal
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerContentContainer:
    """Portal marker creates content in a distinct container via ``_container``."""

    def test_create_in_container(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[
                    {"type": "Folder", "id": "folder", "title": "Folder"},
                    {
                        "type": "Document",
                        "id": "doc1",
                        "title": "Nested",
                        "_container": "/folder",
                    },
                ],
            )
            def test_document_in_folder(portal):
                assert "folder" in portal
                assert "doc1" not in portal
                assert "doc1" in portal["folder"]
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerContentReviewState:
    """Portal marker transitions content via ``_review_state``."""

    def test_create_in_review_state(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            @pytest.mark.portal(
                content=[
                    {
                        "type": "Document",
                        "id": "doc1",
                        "title": "Published",
                        "_review_state": "published",
                    },
                ],
            )
            def test_document_published(portal):
                assert api.content.get_state(obj=portal["doc1"]) == "published"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_content_is_catalogued(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            @pytest.mark.portal(
                content=[
                    {
                        "type": "Document",
                        "id": "doc1",
                        "title": "Published",
                        "_review_state": "published",
                    },
                ],
            )
            def test_document_found_in_catalog(portal):
                results = api.content.find(review_state="published", id="doc1")
                assert len(results) == 1
                assert results[0].getPath().endswith("/doc1")
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_container_and_review_state_combined(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            @pytest.mark.portal(
                content=[
                    {"type": "Folder", "id": "folder", "title": "Folder"},
                    {
                        "type": "Document",
                        "id": "doc1",
                        "title": "Nested Published",
                        "_container": "/folder",
                        "_review_state": "published",
                    },
                ],
            )
            def test_nested_published(portal):
                doc = portal["folder"]["doc1"]
                assert api.content.get_state(obj=doc) == "published"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerContentIndexes:
    """Marker content is applied to the catalog indexes, not just queued.

    Catalog *queries* flush the pending indexing queue themselves, so they
    hide the problem. These tests read an index directly, which does not.
    """

    def test_unique_values_for_sees_every_item(self, testdir):
        # Before the fix this returned ["alpha", "beta"]: the last item
        # created was still queued when the test body ran.
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            CONTENT = [
                {"type": "Document", "id": "doc-1", "title": "Doc 1",
                 "subject": ("alpha",)},
                {"type": "Document", "id": "doc-2", "title": "Doc 2",
                 "subject": ("beta",)},
                {"type": "Document", "id": "doc-3", "title": "Doc 3",
                 "subject": ("gamma",)},
            ]

            @pytest.mark.portal(content=CONTENT)
            def test_unique_values(portal):
                catalog = api.portal.get_tool("portal_catalog")
                got = sorted(catalog.uniqueValuesFor("Subject"))
                assert got == ["alpha", "beta", "gamma"], got
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_unique_values_for_sees_content_in_container(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            CONTENT = [
                {"type": "Folder", "id": "folder", "title": "Folder"},
                {"type": "Document", "id": "doc-1", "title": "Doc 1",
                 "subject": ("alpha",), "_container": "/folder",
                 "_review_state": "published"},
                {"type": "Document", "id": "doc-2", "title": "Doc 2",
                 "subject": ("beta",), "_container": "/folder"},
            ]

            @pytest.mark.portal(content=CONTENT)
            def test_unique_values(portal):
                catalog = api.portal.get_tool("portal_catalog")
                got = sorted(catalog.uniqueValuesFor("Subject"))
                assert got == ["alpha", "beta"], got
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)

    def test_create_content_fixture_flushes_too(self, testdir):
        # The session-scoped ``create_content`` fixture delegates to the same
        # helper, so it gets the flush as well.
        testdir.makepyfile(
            """
            from plone import api

            CONTENT = [
                {"type": "Document", "id": "doc-1", "title": "Doc 1",
                 "subject": ("alpha",)},
                {"type": "Document", "id": "doc-2", "title": "Doc 2",
                 "subject": ("beta",)},
            ]

            def test_unique_values(portal, create_content):
                create_content(portal, CONTENT)
                catalog = api.portal.get_tool("portal_catalog")
                got = sorted(catalog.uniqueValuesFor("Subject"))
                assert got == ["alpha", "beta"], got
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerProfiles:
    """Portal marker applies GenericSetup profiles."""

    def test_apply_profile(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            @pytest.mark.portal(profiles=["plone.app.contenttypes:default"])
            def test_profile_applied(portal):
                setup_tool = api.portal.get_tool("portal_setup")
                # Verify the profile was applied by checking the profile version
                version = setup_tool.getLastVersionForProfile(
                    "plone.app.contenttypes:default"
                )
                assert version is not None
                assert version != "unknown"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerCombined:
    """Portal marker supports combining profiles, content, and roles."""

    def test_profiles_content_and_roles(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
                roles=["Manager"],
            )
            def test_combined(portal):
                assert "doc1" in portal
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Manager" in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=1)


@pytest.mark.no_cover
class TestPortalMarkerIsolation:
    """Marker setup doesn't leak between tests (integration layer rollback)."""

    def test_isolation_between_tests(self, testdir):
        testdir.makepyfile(
            """
            import pytest

            @pytest.mark.portal(
                content=[{"type": "Document", "id": "doc1", "title": "Doc"}],
            )
            def test_first(portal):
                assert "doc1" in portal

            def test_second(portal):
                assert "doc1" not in portal
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)

    def test_roles_do_not_leak(self, testdir):
        # Use "Reviewer", NOT "Manager": the Products.CMFPlone test layer grants
        # the test user "Manager" *globally* by default, so a Manager-based probe
        # would see it in the second test regardless of the marker and wrongly
        # look like a leak. "Reviewer" is not a baseline role, so its presence in
        # the second test would be a genuine leak from the first.
        testdir.makepyfile(
            """
            import pytest
            from plone import api
            from plone.app.testing import TEST_USER_ID

            @pytest.mark.portal(roles=["Reviewer"])
            def test_first(portal):
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Reviewer" in roles

            def test_second(portal):
                roles = api.user.get_roles(username=TEST_USER_ID, obj=portal)
                assert "Reviewer" not in roles
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)

    def test_profiles_do_not_leak(self, testdir):
        testdir.makepyfile(
            """
            import pytest
            from plone import api

            PROFILE = "plone.session:default"

            @pytest.mark.portal(profiles=[PROFILE])
            def test_first(portal):
                st = api.portal.get_tool("portal_setup")
                assert st.getLastVersionForProfile(PROFILE) != "unknown"

            def test_second(portal):
                st = api.portal.get_tool("portal_setup")
                assert st.getLastVersionForProfile(PROFILE) == "unknown"
            """
        )
        result = testdir.runpytest_subprocess()
        result.assert_outcomes(passed=2)
