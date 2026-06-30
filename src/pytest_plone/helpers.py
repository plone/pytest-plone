from collections.abc import Iterable
from plone.testing.layer import Layer
from typing import Any

import pytest
import zope.pytestlayer.fixture


def _keep_session_fixture(session_fixture_name: str):
    """Create an autouse session fixture that pins a layer for the session.

    ``zope.pytestlayer`` only parks a layer in ``keep_for_whole_session`` when
    its session-scoped fixture is requested.  Function-style tests
    (``def test_x(portal): ...``) only depend on the function- and class-scoped
    fixtures, so without this the layer is torn down and set up again -- running
    a full ``applyProfile`` -- around *every single test*.

    Requesting the ``{prefix}_session`` fixture once, via an autouse session
    fixture, keeps the (expensive) layer set up for the whole session.  Per-test
    isolation is unaffected: ``IntegrationTesting`` still rolls back the
    transaction after each test.
    """

    @pytest.fixture(autouse=True, scope="session")
    def _keep_layer_for_session(request):
        request.getfixturevalue(session_fixture_name)

    return _keep_layer_for_session


def fixtures_factory(
    test_layers: Iterable[tuple[Layer, str]],
    *,
    keep_session: bool = True,
) -> dict[str, Any]:
    """Create pytest fixtures for a group of plone.testing.layer.Layer.

    :param test_layers: Iterable (tuple or list) containing two-element tuple with
                        the Layer object and a string with the prefix to use for
                        fixtures created for that layer.
    :param keep_session: When ``True`` (the default) an autouse session fixture is
                        registered per layer so the layer is set up once per
                        session instead of once per function-style test.  Set to
                        ``False`` to restore the previous behavior.

    ```python
        fixtures_factory(
            (
                (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
                (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
            )
        )
    ```
    """
    fixtures = {}
    for layer, prefix in test_layers:
        fixtures.update(
            zope.pytestlayer.fixture.create(
                layer,
                session_fixture_name=f"{prefix}_session",
                class_fixture_name=f"{prefix}_class",
                function_fixture_name=prefix,
            )
        )
        if keep_session:
            fixtures[f"_keep_{prefix}_session"] = _keep_session_fixture(
                f"{prefix}_session"
            )
    return fixtures
