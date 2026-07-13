"""Committed functional-layer changes are isolated per test.

The ``portal`` marker (and any test that stages content) relies on the testing
layer to undo its changes after each test.  For plain integration/ORM tests
that is the per-test ``transaction.abort()``.  The harder case is a *functional*
test that **commits** — needed so a real HTTP request, served on a separate
thread and ZODB connection, can see the content.  This module proves that even
in that case ``FunctionalTesting`` discards the committed data at teardown (via
its stacked ``DemoStorage``), so nothing leaks into the next test.

A committing marker would therefore need no explicit teardown: the layer already
undoes the change.  These tests lock that guarantee in.
"""

import pytest


# A functional layer with a real WSGI server so ``absolute_url()`` is reachable
# over HTTP.  ``PLONE_FIXTURE`` keeps it lightweight; we only need traversal.
SERVER_CONFTEST = """
    from plone.app.testing import FunctionalTesting
    from plone.app.testing import PLONE_FIXTURE
    from plone.testing.zope import WSGI_SERVER_FIXTURE
    from pytest_plone import fixtures_factory

    pytest_plugins = ["pytest_plone"]

    SERVER_FUNCTIONAL = FunctionalTesting(
        bases=(PLONE_FIXTURE, WSGI_SERVER_FIXTURE),
        name="pytest_plone:ServerFunctional",
    )

    globals().update(fixtures_factory(((SERVER_FUNCTIONAL, "functional"),)))
"""

COMMIT_AND_FETCH = """
    import requests
    import transaction
    from plone import api
    from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

    def _get(portal, path):
        return requests.get(
            f"{portal.absolute_url()}/{path}",
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    def test_first_commits_and_serves(functional_portal):
        portal = functional_portal
        with api.env.adopt_user(SITE_OWNER_NAME):
            api.content.create(
                container=portal, type="Document", id="doc1", title="D"
            )
        transaction.commit()
        # The real HTTP server (separate connection) sees the committed content.
        assert _get(portal, "doc1").status_code == 200

    def test_second_does_not_see_it(functional_portal):
        portal = functional_portal
        # Committed data from the previous test was discarded at teardown.
        assert "doc1" not in portal
        assert _get(portal, "doc1").status_code == 404
"""


@pytest.mark.no_cover
def test_committed_functional_change_is_isolated(testdir):
    testdir.makeconftest(SERVER_CONFTEST)
    testdir.makepyfile(COMMIT_AND_FETCH)
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=2)
