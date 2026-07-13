"""Fixtures used in add-on install / uninstall tests."""

from plone import api
from plone.base.utils import get_installer
from plone.browserlayer import utils
from Products.CMFPlone.controlpanel.browser.quickinstaller import InstallerView
from Products.CMFPlone.Portal import PloneSite
from Products.GenericSetup.tool import SetupTool
from pytest_plone import _types as t
from pytest_plone.fixtures import markers
from zope.interface.interface import InterfaceClass

import pytest


@pytest.fixture
def installer(portal: PloneSite) -> InstallerView:
    """Portal helper for managing add-ons using GenericSetup.

    Example usage:
    ```python
    PACKAGE_NAME = "collective.person"

    class TestSetupUninstall:
        @pytest.fixture(autouse=True)
        def uninstalled(self, installer):
            installer.uninstall_product(PACKAGE_NAME)
    ```
    """
    return get_installer(portal)


@pytest.fixture
def uninstalled(installer: InstallerView, package_name: str) -> None:
    """Uninstall the add-on under test from the current portal.

    Requires a ``package_name`` fixture defined in your ``conftest.py``
    that returns the distribution name of the add-on being tested.

    Example usage:
    ```python
    # conftest.py
    import pytest


    @pytest.fixture
    def package_name() -> str:
        return "collective.person"


    # tests/test_setup.py
    class TestSetupUninstall:
        @pytest.fixture(autouse=True)
        def uninstalled(self, uninstalled):
            # add-on is now uninstalled for every test in this class
            pass

        def test_product_uninstalled(self, installer, package_name):
            assert installer.is_product_installed(package_name) is False
    ```
    """
    installer.uninstall_product(package_name)


@pytest.fixture
def browser_layers(portal: PloneSite) -> list[InterfaceClass]:
    """List of browser layers registered in a portal.

    Example usage:
    ```python
    def test_browserlayer(browser_layers):
        from collective.person.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers
    ```
    """
    return utils.registered_layers()


@pytest.fixture
def controlpanel_actions(portal: PloneSite) -> list[str]:
    """List of identifiers (id) of control panel actions.

    Example usage:
    ```python
    def test_controlpanel_installed(controlpanel_actions):
        assert "MyControlPanel" in controlpanel_actions
    ```
    """
    controlpanel = portal.portal_controlpanel
    return [a.getAction(portal)["id"] for a in controlpanel.listActions()]


@pytest.fixture
def setup_tool(portal: PloneSite) -> SetupTool:
    """Return the portal_setup for the current portal.

    Example usage:
    ```python
    def test_profile_version(setup_tool):
        name = "profile-collective.person:default"
        version = setup_tool.getLastVersionForProfile(name)
        assert version[0] == "1000"
    ```
    """
    return api.portal.get_tool("portal_setup")


@pytest.fixture
def profile_last_version(setup_tool: SetupTool) -> t.ProfileVersionGetter:
    """Provides a method to return the last version for a profile.

    Example usage:
    ```python
    PACKAGE_NAME = "collective.person"

    def test_latest_version(profile_last_version):
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1000"
    ```
    """

    def profile_last_version(profile: str) -> str:
        """Return the last version for a profile."""
        version = setup_tool.getLastVersionForProfile(profile)
        return version[0] if version else ""

    return profile_last_version


@pytest.fixture(scope="session")
def apply_profiles() -> t.ProfilesApplier:
    """Apply GenericSetup profiles to a Plone site.

    Example usage:
    ```python
    def test_with_profile(portal, apply_profiles):
        apply_profiles(portal, ["my.addon:testing"])
    ```
    """

    def func(portal: PloneSite, profiles: list[str]) -> None:
        markers.apply_profiles(portal, profiles)

    return func
