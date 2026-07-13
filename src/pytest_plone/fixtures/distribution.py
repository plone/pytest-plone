from OFS.Application import Application
from plone import api
from plone.distribution.api import site as site_api
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import _types as t
from typing import Any
from zope.component.hooks import setSite

import pytest


TEST_LOGO = """filenameb64:dGVzdC1sb2dvLnN2Zw==;datab64:PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIGlkPSJMYXllcl8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjE1OC4yNTNweCIgaGVpZ2h0PSI0MC42ODZweCIgdmlld0JveD0iMCAwIDE1OC4yNTMgNDAuNjg2IiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCAxNTguMjUzIDQwLjY4NiIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CiAgPGcgZmlsbD0iIzAyMTMyMiI+CiAgICA8cGF0aCBkPSJNNjUuMzI3LDIzLjIwOGgtNi41ODl2MTEuMzg4aC00LjM5M1Y1LjYzOGgxMC45ODFjNS42NTMsMCw5LjI3MSwzLjc0Miw5LjI3MSw4Ljc4NSAgICAgICAgICAgICAgICAgUzcwLjk3OSwyMy4yMDgsNjUuMzI3LDIzLjIwOHogTTY1LjA4Miw5LjU4M2gtNi4zNDV2OS42MzloNi4zNDVjMy4wNSwwLDUuMTI0LTEuNzQ5LDUuMTI0LTQuNzk5ICAgICAgICAgICAgICAgICBDNzAuMjA2LDExLjM3Miw2OC4xMzIsOS41ODMsNjUuMDgyLDkuNTgzeiIvPgogICAgPHBhdGggZD0iTTgzLjk2OSwzNC41OTZjLTMuOTA0LDAtNS42NTItMi42NDQtNS42NTItNS42OTNWNS42MzhoNC4xNDh2MjMuMDIxYzAsMS41ODcsMC41NjcsMi4zOTksMi4yMzUsMi4zOTloMS44MyAgICAgICAgICAgICAgICAgdjMuNTM4SDgzLjk2OXoiLz4KICAgIDxwYXRoIGQ9Ik0xMDQuNzYyLDMyLjM5OWMtMS4zNDQsMS4zODQtMy4zNzcsMi40NC02LjE4NCwyLjQ0Yy0yLjgwNSwwLTQuNzk5LTEuMDU4LTYuMTQxLTIuNDQgICAgICAgICAgICAgICAgIGMtMS45NTEtMi4wMzItMi40MzktNC42MzctMi40MzktOC4xMzRjMC0zLjQ1NywwLjQ4OC02LjA2MSwyLjQzOS04LjA5NGMxLjM0Mi0xLjM4MywzLjMzNi0yLjQ0LDYuMTQxLTIuNDQgICAgICAgICAgICAgICAgIGMyLjgwNywwLDQuODQsMS4wNTksNi4xODQsMi40NGMxLjk1MSwyLjAzMywyLjQzOSw0LjYzNywyLjQzOSw4LjA5NEMxMDcuMjAzLDI3Ljc2MywxMDYuNzEzLDMwLjM2NiwxMDQuNzYyLDMyLjM5OXogICAgICAgICAgICAgICAgICBNMTAxLjYyOSwxOC42MTNjLTAuNzczLTAuNzczLTEuODMtMS4xODEtMy4wNTEtMS4xODFjLTEuMjE5LDAtMi4yMzYsMC40MDYtMy4wMSwxLjE4MWMtMS4yNiwxLjI2MS0xLjQyMiwzLjQxNi0xLjQyMiw1LjY1MiAgICAgICAgICAgICAgICAgczAuMTYyLDQuMzkzLDEuNDIyLDUuNjUzYzAuNzczLDAuNzcxLDEuNzkxLDEuMjIsMy4wMSwxLjIyYzEuMjIxLDAsMi4yNzctMC40NDcsMy4wNTEtMS4yMmMxLjI2Mi0xLjI2MiwxLjQyNC0zLjQxNywxLjQyNC01LjY1MyAgICAgICAgICAgICAgICAgUzEwMi44OTEsMTkuODczLDEwMS42MjksMTguNjEzeiIvPgogICAgPHBhdGggZD0iTTEyMy42NDMsMzQuNTk2VjIyLjAyOWMwLTMuMjE0LTEuODMtNC41OTctNC4xNDctNC41OTdzLTQuMjcxLDEuNDIzLTQuMjcxLDQuNTk3djEyLjU2NmgtNC4xNDd2LTIwLjYyICAgICAgICAgICAgICAgICBoNC4wNjV2Mi4wNzRjMS40MjUtMS41NDYsMy40MTYtMi4zMTgsNS40OS0yLjMxOGMyLjExNSwwLDMuODY1LDAuNjkxLDUuMDg0LDEuODcxYzEuNTg2LDEuNTQ1LDIuMDc0LDMuNDk3LDIuMDc0LDUuODE1djEzLjE3OCAgICAgICAgICAgICAgICAgTDEyMy42NDMsMzQuNTk2TDEyMy42NDMsMzQuNTk2eiIvPgogICAgPHBhdGggZD0iTTEzNS43NzIsMjUuNDg2YzAsMy41MzcsMS44NzEsNS43NzQsNS4yNDYsNS43NzRjMi4zMTcsMCwzLjUzOS0wLjY0OSw1LjAwNC0yLjExNWwyLjY0MywyLjQ4MSAgICAgICAgICAgICAgICAgYy0yLjExNSwyLjExNC00LjEwNywzLjIxMy03LjcyNywzLjIxM2MtNS4xNjYsMC05LjI3My0yLjcyNS05LjI3My0xMC41NzRjMC02LjY3MSwzLjQ1Ny0xMC41MzQsOC43NDQtMTAuNTM0ICAgICAgICAgICAgICAgICBjNS41MzEsMCw4Ljc0NCw0LjA2Nyw4Ljc0NCw5LjkyNXYxLjgzSDEzNS43NzJ6IE0xNDQuNDc1LDE5Ljc5MWMtMC42NS0xLjU0NS0yLjExMy0yLjYwNC00LjA2Ni0yLjYwNCAgICAgICAgICAgICAgICAgYy0xLjk1MSwwLTMuNDU3LDEuMDU5LTQuMTA3LDIuNjA0Yy0wLjQwNiwwLjkzNi0wLjQ4OCwxLjU0Ni0wLjUyOSwyLjgwN2g5LjI3M0MxNDUuMDAzLDIxLjMzNywxNDQuODgzLDIwLjcyNiwxNDQuNDc1LDE5Ljc5MXoiLz4KICAgIDxjaXJjbGUgY3g9IjE3LjgxNSIgY3k9IjExLjUxNiIgcj0iNC40MDIiLz4KICAgIDxwYXRoIGQ9Ik0zMS4xNjcsMjAuMzExYzAsMi40MzMtMS45NjksNC40MDEtNC40MDMsNC40MDFjLTIuNDI3LDAtNC40MDEtMS45Ny00LjQwMS00LjQwMSAgICAgICAgICAgICAgICAgYzAtMi40MzMsMS45NzUtNC40MDEsNC40MDEtNC40MDFDMjkuMiwxNS45MDksMzEuMTY3LDE3Ljg3OSwzMS4xNjcsMjAuMzExeiIvPgogICAgPGNpcmNsZSBjeD0iMTcuODAxIiBjeT0iMjkuMTMxIiByPSI0LjQwMiIvPgogICAgPGc+CiAgICAgIDxwYXRoIGQ9Ik0yMC40NDEtMC4wNDVDOS4yMDctMC4wNDQsMC4xLDkuMDYzLDAuMDk5LDIwLjI5OEMwLjEsMzEuNTMyLDkuMjA3LDQwLjYzOSwyMC40NDEsNDAuNjQxICAgICAgICAgICAgICAgICAgICAgYzExLjIzNS0wLjAwMiwyMC4zNDEtOS4xMDcsMjAuMzQzLTIwLjM0M0M0MC43ODMsOS4wNjMsMzEuNjc3LTAuMDQ0LDIwLjQ0MS0wLjA0NXogTTMxLjg5MSwzMS43NDcgICAgICAgICAgICAgICAgICAgICBjLTIuOTM3LDIuOTM0LTYuOTcyLDQuNzQyLTExLjQ1LDQuNzQzYy00LjQ3OC0wLjAwMS04LjUxMy0xLjgxMS0xMS40NS00Ljc0M0M2LjA1OCwyOC44MSw0LjI1LDI0Ljc3NSw0LjI0OSwyMC4yOTggICAgICAgICAgICAgICAgICAgICBjMC4wMDEtNC40NzgsMS44MDktOC41MTMsNC43NDMtMTEuNDVjMi45MzctMi45MzQsNi45NzItNC43NDIsMTEuNDUtNC43NDNjNC40NzgsMC4wMDEsOC41MTMsMS44MSwxMS40NSw0Ljc0MyAgICAgICAgICAgICAgICAgICAgIGMyLjkzNCwyLjkzOCw0Ljc0Miw2Ljk3Myw0Ljc0MywxMS40NUMzNi42MzMsMjQuNzc1LDM0LjgyNSwyOC44MSwzMS44OTEsMzEuNzQ3eiIvPgogICAgPC9nPgogICAgPGc+CiAgICAgIDxwYXRoIGQ9Ik0xNTMuOTg1LDkuOTVjLTEuMTk1LDAtMi4xNjQsMC45NzEtMi4xNjQsMi4xNjhjMC4wMDIsMS4xOTcsMC45NjksMi4xNjgsMi4xNjQsMi4xNjggICAgICAgICAgICAgICAgICAgICBjMS4xOTksMCwyLjE3Mi0wLjk3MSwyLjE3Mi0yLjE2OFMxNTUuMTg0LDkuOTUsMTUzLjk4NSw5Ljk1eiBNMTUzLjk4NSwxMy45NjhjLTEuMDIxLTAuMDAyLTEuODQ2LTAuODI3LTEuODQ2LTEuODUgICAgICAgICAgICAgICAgICAgICBjMC4wMDItMS4wMjEsMC44MjUtMS44NDksMS44NDYtMS44NTFjMS4wMjMsMC4wMDIsMS44NTIsMC44MjgsMS44NTQsMS44NTFDMTU1LjgzNiwxMy4xNDEsMTU1LjAwOCwxMy45NjYsMTUzLjk4NSwxMy45Njh6Ii8+CiAgICA8L2c+CiAgICA8Zz4KICAgICAgPHBhdGggZD0iTTE1NC41MDcsMTMuNDA5bC0wLjU0LTEuMDhoLTAuNDg2djEuMDhoLTAuMzg5di0yLjU2NGgwLjk5NGMwLjQ4NCwwLDAuNzk2LDAuMzEzLDAuNzk2LDAuNzUgICAgICAgICAgICAgICAgICAgICBjMCwwLjM2Ny0wLjIyNCwwLjYwMi0wLjUxMywwLjY4bDAuNTkyLDEuMTM2TDE1NC41MDcsMTMuNDA5TDE1NC41MDcsMTMuNDA5eiBNMTU0LjA1NiwxMS4xOTVoLTAuNTc1djAuODAzaDAuNTc1IGMwLjI2MSwwLDAuNDM3LTAuMTQ3LDAuNDM3LTAuMzk5UzE1NC4zMTcsMTEuMTk1LDE1NC4wNTYsMTEuMTk1eiIvPgogICAgPC9nPgogIDwvZz4KPC9zdmc+Cg=="""  # noqa: E501


@pytest.fixture(scope="session")
def site_logo() -> str:
    """Return a data-URI logo usable as the ``site_logo`` answer.

    :returns: an SVG image encoded as a ``data:`` URI.
    """
    return TEST_LOGO


@pytest.fixture(scope="session")
def answers(site_logo: str) -> dict:
    """Return the default answers for creating a distribution site.

    Override this fixture on your tests to change the answers
    for creating a Plone site from a distribution.

    :param site_logo: data-URI logo injected as the ``site_logo`` answer.
    :returns: a mapping of answers passed to the distribution site handler.
    """
    return {
        "site_id": "plone-site",
        "title": "Plone Site",
        "description": "New site.",
        "default_language": "en",
        "portal_timezone": "UTC",
        "site_logo": site_logo,
        "setup_content": False,
    }


@pytest.fixture(scope="session")
def distribution_name() -> str:
    """Return the name of the distribution to create sites from.

    Override this fixture on your tests to change the distribution used
    for creating Plone sites with the fixture `create_site`.

    :returns: the distribution name.
    """
    return "testing"


@pytest.fixture(scope="session")
def create_site(distribution_name: str, site_owner_name: str) -> t.SiteCreator:
    """Return a callable that creates a Plone site from a distribution.

    The returned callable creates a **new** site in *app* from the
    *distribution_name* distribution, deleting any existing site with the same
    ``site_id`` first to guarantee a clean state, and sets it as the current
    local site. The created site coexists with the site provided by the testing
    layer (a second site, by design).

    :param distribution_name: distribution the site is created from.
    :param site_owner_name: login of the site owner the site is created as.
    :returns: a callable ``func(app, answers) -> PloneSite``.
    """

    def func(app: Application, answers: dict[str, Any]) -> PloneSite:
        with api.env.adopt_user(site_owner_name):
            # Delete site if it already exists to ensure a clean state
            if (site_id := answers.get("site_id")) and site_id in app.objectIds():
                app.manage_delObjects([site_id])
            # Use _create_site to avoid committing the changes
            site = site_api._create_site(
                context=app,
                distribution_name=distribution_name,
                answers=answers,
            )
            setSite(site)
        return site

    return func
