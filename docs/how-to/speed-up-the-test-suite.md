# How to speed up a slow test suite

This guide shows you how to diagnose and fix the common causes of a slow Plone test suite.

## Find out where the time goes

Run the suite with durations reporting:

```shell
pytest --durations=0
```

Read the **phase** column, not just the numbers.
pytest reports `setup`, `call`, and `teardown` separately, and which one dominates tells you what to fix.

- Time in **call** means your tests are genuinely doing slow work.
- Time in **setup** means the machinery around your tests is the problem. Read on.

## Rule out layer thrashing

If the costly entries are all in `setup` and each costs roughly the same couple of seconds, the testing layer is being torn down and rebuilt around every test.

This is the single most expensive mistake available to you — it has been measured at a twenty-fold slowdown.

`fixtures_factory` prevents it by default by keeping each layer set up for the whole session.
If you see this symptom, check that you have not disabled that:

```python
fixtures_factory(layers, keep_session=False)   # <- this reintroduces the problem
```

Remove the `keep_session=False`.

{doc}`/explanation/layers-scopes-and-isolation` explains why this happens at all.

## Share an expensive portal across a test class

When a group of tests needs the same costly setup — a portal with a profile applied and content created — build it once for the class rather than once per test.

Use the class-scoped fixtures and put the marker on the class:

```python
import pytest


@pytest.mark.portal(
    profiles=["my.addon:testing"],
    content=[{"type": "Document", "id": "doc1", "title": "A document"}],
)
class TestDocumentViews:
    def test_doc_exists(self, portal_class):
        assert "doc1" in portal_class

    def test_doc_title(self, portal_class):
        assert portal_class["doc1"].title == "A document"
```

```{warning}
Class-scoped fixtures trade isolation for speed.
The tests in the class share one portal, so state created by one method is visible to the next, and a test that mutates the portal can break the one after it.
Use this when the tests only read, or when the shared state is the point.
```

## Run tests in parallel

`pytest-xdist` distributes tests across processes:

```shell
pytest -n auto
```

Each worker sets up its own layer, so this trades memory for wall-clock time.
It pays off on suites with many tests and hurts on small ones.

## Skip work you do not need

The functional layer is more expensive than the integration layer, because it commits real transactions instead of aborting them.
Only reach for `functional_portal` and friends when a real HTTP request has to reach a running server.
For everything in-process, use `portal`.
