"""Fixtures provided by pytest-plone."""

from .addons import apply_profiles
from .addons import browser_layers
from .addons import controlpanel_actions
from .addons import installer
from .addons import profile_last_version
from .addons import setup_tool
from .addons import uninstalled
from .base import app
from .base import app_class
from .base import functional_app
from .base import functional_app_class
from .base import functional_http_request
from .base import functional_portal
from .base import functional_portal_class
from .base import http_request
from .base import portal
from .base import portal_class
from .base import site_owner_name
from .base import site_owner_password
from .content import create_content
from .content import get_behaviors
from .content import get_fti
from .distribution import answers
from .distribution import create_site
from .distribution import distribution_name
from .distribution import site_logo
from .env import generate_mo
from .requests import anon_request
from .requests import manager_request
from .requests import request_factory
from .security import grant_roles
from .vocabularies import get_vocabulary

import pytest


__all__ = [
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
    "uninstalled",
]


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "portal(profiles=None, content=None, roles=None): "
        "configure the portal fixture with GenericSetup profiles, "
        "pre-created content, and/or user roles",
    )
