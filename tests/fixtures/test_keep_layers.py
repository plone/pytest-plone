"""Tests for session-wide keep of the testing layers.

With function-style tests the layer ``setUp`` (including ``applyProfile``) must
run *once per session*, not once per test.  ``zope.pytestlayer`` only keeps a
layer for the whole session when its session-scoped fixture is pulled in, which
function tests never do on their own.  ``fixtures_factory`` therefore registers
an autouse session fixture per layer (unless ``keep_session=False``).

The layer name is printed by ``zope.pytestlayer`` once per ``setUp`` (see
``zope.pytestlayer.fixture.setup_layer``), so we count those lines to tell a
single session-wide setup apart from per-test layer thrashing.
"""

import pytest


INTEGRATION_LAYER = "Products.CMFPlone.testing.PRODUCTS_CMFPLONE_INTEGRATION_TESTING"

THREE_FUNCTION_TESTS = """
    def test_one(portal):
        assert portal.title == "Plone site"

    def test_two(portal):
        assert portal.title == "Plone site"

    def test_three(portal):
        assert portal.title == "Plone site"
"""


def _count_setups(result, layer_name: str) -> int:
    """Count how often ``layer_name`` was set up during the run."""
    return [line.strip() for line in result.outlines].count(layer_name)


@pytest.mark.no_cover
def test_layer_kept_for_whole_session(testdir):
    """Three function tests set the integration layer up only once."""
    testdir.makepyfile(THREE_FUNCTION_TESTS)
    result = testdir.runpytest_subprocess("-s")
    result.assert_outcomes(passed=3)
    assert _count_setups(result, INTEGRATION_LAYER) == 1


@pytest.mark.no_cover
def test_layer_not_kept_when_opted_out(testdir_no_keep):
    """With ``keep_session=False`` the old per-test behavior is preserved."""
    testdir_no_keep.makepyfile(THREE_FUNCTION_TESTS)
    result = testdir_no_keep.runpytest_subprocess("-s")
    result.assert_outcomes(passed=3)
    # No session keep -> layer thrashes: one setup per function test.
    assert _count_setups(result, INTEGRATION_LAYER) == 3
