# How to test a REST API endpoint

This guide shows you how to test a `plone.restapi` service with real HTTP requests.

REST API tests need the **functional** layer.
A real request arrives over the network in a different transaction, so it cannot see anything your test has not committed — which is exactly what the integration layer never does.

## Make an anonymous request

[`anon_request`](/reference/fixtures.md#requests) is a session bound to the portal with no authentication.
Relative URLs resolve against the portal's REST API root, so you can ask for `/` and mean the site.

```python
def test_root_is_public(anon_request):
    response = anon_request.get("/")

    assert response.status_code == 200
    assert response.json()["@type"] == "Plone Site"
```

## Make an authenticated request

[`manager_request`](/reference/fixtures.md#requests) is authenticated as the site owner.

```python
def test_controlpanels_require_auth(manager_request):
    response = manager_request.get("/@controlpanels")

    assert response.status_code == 200
```

## Use other credentials

For any identity other than the two shorthands, build a session yourself with [`request_factory`](/reference/fixtures.md#requests).

```python
def test_as_specific_user(request_factory):
    session = request_factory(basic_auth=("editor", "secret"))

    response = session.get("/")

    assert response.status_code == 200
```

To talk to the site outside the REST API traverser, pass `api=False`:

```python
def test_html_view(request_factory):
    session = request_factory(role="Manager", api=False)

    response = session.get("/")

    assert "<html" in response.text
```

## Create content to test against

The functional portal is a normal portal.
Put content on it with the marker, and it is there when the request arrives.

```python
import pytest


@pytest.mark.portal(
    content=[{"type": "Document", "id": "doc1", "title": "A document"}],
)
def test_get_document(functional_portal, anon_request):
    response = anon_request.get("/doc1")

    assert response.status_code == 200
    assert response.json()["title"] == "A document"
```

```{important}
Request the `functional_portal` fixture in the test even if you do not use the object.
It is what builds the portal the marker acts on, and what the session's base URL points at.
```

## Share a portal across a REST API suite

REST API suites are usually read-only, which makes them a good fit for the class-scoped fixture — one portal, built once, for the whole class.

```python
import pytest


@pytest.mark.portal(roles=["Manager"])
class TestSearchService:
    def test_search_returns_results(self, functional_portal_class, manager_request):
        response = manager_request.get("/@search")

        assert response.status_code == 200
```

See {doc}`speed-up-the-test-suite` for the trade-off this makes.
