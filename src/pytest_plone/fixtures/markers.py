"""Marker support for pytest-plone fixtures."""

from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFPlone.Portal import PloneSite
from zope.component.hooks import site

import pytest


PORTAL_MARKER_NAME: str = "portal"


def apply_profiles(portal: PloneSite, profiles: list[str]) -> None:
    """Apply GenericSetup profiles to a Plone site.

    Each entry can be either ``"my.addon:default"`` or the full
    ``"profile-my.addon:default"`` form — the ``profile-`` prefix
    is added automatically when missing.
    """
    with site(portal):
        setup_tool = api.portal.get_tool("portal_setup")
        for profile_id in profiles:
            if not profile_id.startswith("profile-"):
                profile_id = f"profile-{profile_id}"
            setup_tool.runAllImportStepsFromProfile(profile_id)


def create_content(portal: PortalContent, content: list[dict]) -> list[PortalContent]:
    """Create content items, optionally in a distinct container and review state.

    Each entry in *content* is a mapping passed as keyword arguments to
    :func:`plone.api.content.create`. Two keys receive special handling and
    are consumed before the call:

    - ``_container``: path to the container the item is created in, relative to
      the site root as understood by :func:`plone.api.content.get`
      (e.g. ``"/folder"``). Defaults to *portal* when absent.
    - ``_review_state``: target workflow state; the created item is transitioned
      to it via :func:`plone.api.content.transition`.

    :param portal: default container used when a spec omits ``_container``.
    :param content: list of content specifications.
    :returns: the created content items, in creation order.
    """
    items = []
    for spec in content:
        # Copy so the special keys we pop below don't mutate the marker's
        # dicts, which are reused across parametrized runs of the same test.
        spec = dict(spec)
        container = portal
        # Get the container for the content item.
        if container_path := spec.pop("_container", None):
            container = api.content.get(path=container_path)
        # If a review state is specified, we transition the content to
        # that state after creation.
        to_state = spec.pop("_review_state", None)
        item = api.content.create(container=container, **spec)
        if to_state is not None:
            api.content.transition(obj=item, to_state=to_state)
        items.append(item)
    # Force a reindex: content created here has been observed to stay stale in
    # the catalog (not returned by queries) until reindexed explicitly.
    for item in items:
        item.reindexObject()
    return items


def grant_roles(context: PortalContent, roles: list[str]) -> None:
    """Grant roles to the default test user."""
    api.user.grant_roles(username=TEST_USER_ID, roles=roles, obj=context)


def apply_portal_marker(portal: PloneSite, request: pytest.FixtureRequest) -> None:
    """Read ``@pytest.mark.portal`` and apply profiles, content, and roles."""
    marker = request.node.get_closest_marker(PORTAL_MARKER_NAME)
    if marker is None:
        return
    marker_profiles: list[str] = marker.kwargs.get("profiles", [])
    marker_content: list[dict] = marker.kwargs.get("content", [])
    marker_roles: list[str] = marker.kwargs.get("roles", [])
    with site(portal):
        if marker_profiles:
            apply_profiles(portal, marker_profiles)
        if marker_content:
            with api.env.adopt_user(SITE_OWNER_NAME):
                create_content(portal, marker_content)
        if marker_roles:
            grant_roles(portal, marker_roles)
