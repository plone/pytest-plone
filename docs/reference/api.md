---
myst:
  html_meta:
    "description": "fixtures_factory turns plone.testing layers into pytest fixtures."
    "property=og:description": "fixtures_factory turns plone.testing layers into pytest fixtures."
    "property=og:title": "pytest-plone API"
    "keywords": "Plone, pytest, fixtures_factory, testing layers"
---

# API

## `fixtures_factory`

`fixtures_factory` is the one function you call yourself.
It takes your `plone.testing` layers and returns a dictionary of pytest fixtures, which you inject into your `conftest.py` namespace.

```{autodoc2-object} pytest_plone.helpers.fixtures_factory
render_plugin = "myst"
```

### Generated fixtures

For each `(layer, prefix)` pair you pass, three fixtures are generated:

| Fixture | Scope | Purpose |
| --- | --- | --- |
| `{prefix}` | Function | The layer, with `testSetUp` and `testTearDown` run around each test. |
| `{prefix}_class` | Class | The layer, set up once per test class. |
| `{prefix}_session` | Session | The layer, kept for the whole session. |

With the conventional prefixes `integration` and `functional`, that yields:

| Fixture | Scope |
| --- | --- |
| `integration` | Function |
| `integration_class` | Class |
| `integration_session` | Session |
| `functional` | Function |
| `functional_class` | Class |
| `functional_session` | Session |

The fixtures in {doc}`fixtures` are built on these.
You rarely request them directly — ask for `portal` rather than `integration`.

### Session-wide layers

By default, `fixtures_factory` also registers an autouse session fixture per layer.
This keeps each testing layer set up **once per session** instead of once per test.

The default matters.
Function-style tests depend only on the function- and class-scoped fixtures, never on the session fixture.
Without the autouse fixture, `zope.pytestlayer` tears the layer down and sets it up again — running a full `applyProfile` — around *every single test*.

Per-test isolation is unaffected: `IntegrationTesting` still rolls back the transaction after each test.

To restore the previous behavior, pass `keep_session=False`:

```python
globals().update(
    fixtures_factory(
        (
            (PRODUCTS_CMFPLONE_FUNCTIONAL_TESTING, "functional"),
            (PRODUCTS_CMFPLONE_INTEGRATION_TESTING, "integration"),
        ),
        keep_session=False,
    )
)
```

For the reasoning behind this, see {doc}`/explanation/layers-scopes-and-isolation`.
