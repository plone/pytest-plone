---
myst:
  html_meta:
    "description": "How plone.testing layers become pytest fixtures, and how test isolation actually works."
    "property=og:description": "How plone.testing layers become pytest fixtures, and how test isolation actually works."
    "property=og:title": "About testing layers, scopes, and isolation"
    "keywords": "Plone, pytest, testing layers, zope.pytestlayer, isolation, DemoStorage"
---

# About testing layers, scopes, and isolation

Setting up a Plone site is expensive.
Installing the core profile, registering components, building the catalog — it takes seconds, and seconds multiplied by a test suite is minutes you spend waiting.

Everything in this page follows from that one fact.

## Layers exist to amortize setup

Plone's answer, long predating pytest, is the **testing layer**.
A layer is an object with a `setUp` that builds an expensive thing, a `tearDown` that disposes of it, and a `testSetUp`/`testTearDown` pair that runs around each individual test.

The split is the whole point.
`setUp` runs once and does the costly work.
`testSetUp` runs constantly and does only the cheap work needed to isolate one test from the next.

Layers stack.
`PRODUCTS_CMFPLONE_INTEGRATION_TESTING` sits on top of a layer that created the Plone site, which sits on top of one that started Zope.
Each layer in the chain is set up once, and everything above it reuses the result.

Layers are not something `pytest-plone` invents.
They come from your add-on: by convention you declare them in a `testing.py` module, building on the fixtures `plone.app.testing` provides, and there you say which ZCML to load and which profile to install.
`pytest-plone` does not replace any of that — it consumes the layers you already have.

```{seealso}
The layer machinery itself is documented by the packages that own it:

- [plone.app.testing](https://github.com/plone/plone.app.testing/blob/master/README.rst) — the Plone-specific layers and fixtures, and how to write your own `testing.py`.
- [plone.testing](https://github.com/plone/plone.testing/blob/master/src/plone/testing/README.rst) — the underlying layer model.
```

## How isolation actually works

If the site is built once and shared, why does one test not see another's content?

Because the isolation happens in `testSetUp`/`testTearDown`, not in `setUp`/`tearDown`.

The `IntegrationTesting` layer begins a transaction before each test and **aborts** it afterwards.
Whatever your test created, modified, or deleted is rolled back.
The next test sees the pristine site.

`FunctionalTesting` isolates differently.
It stacks a `DemoStorage` on top of the database, lets the test commit real transactions, and then throws the whole stacked storage away.
That is more expensive, and it is what you need when a real HTTP request has to reach a real running server — a REST API test cannot see your uncommitted transaction.

The practical rule:

- **Integration** for anything you can do in-process. Most tests.
- **Functional** for anything that goes over the wire.

## Layers become fixtures

`zope.pytestlayer` maps this model onto pytest by generating three fixtures per layer, one for each pytest scope:

| Fixture | pytest scope | What it does |
| --- | --- | --- |
| `{prefix}_session` | Session | Sets the layer up and keeps it for the whole run. |
| `{prefix}_class` | Class | Sets the layer up if it is not already up. |
| `{prefix}` | Function | Runs `testSetUp` before and `testTearDown` after each test. |

The function-scoped fixture depends on the class-scoped one, which is how the layer comes to be set up at all.

## The trap this creates

`zope.pytestlayer` decides whether to tear a layer down using two sets it maintains: `keep` and `keep_for_whole_session`.
After each test, the class-scoped fixture's finalizer asks: is my layer in either set?
If not, it tears the layer down.

A layer lands in `keep_for_whole_session` only when its **session-scoped** fixture is requested.

Now consider a plain function-style test:

```python
def test_portal_title(portal):
    assert portal.title == "Plone site"
```

`portal` depends on `integration`, which depends on `integration_class`.
Nothing in that chain touches `integration_session`.
So the layer is never parked in `keep_for_whole_session`, the finalizer finds it in neither set, and it tears the layer down.

The next test sets it up again.
From scratch.
Including `applyProfile`.

The other set, `keep`, is populated from a test item's `.layer` attribute — which only `unittest.TestCase` classes in the classic `zope.testrunner` style carry.
Function-style tests have no `.layer`, so that path never fires for them either.

The result is a full layer teardown and setup around every single test.
On a real suite this was measured at roughly a twenty-fold slowdown: 275 seconds where 14 would do.

It is a quiet failure.
Nothing errors, nothing warns.
The tests pass — they are simply slow, and the slowness looks like Plone being Plone.

The tell is in `pytest --durations=0`: the expensive entries sit in the **setup** phase, not in **call**.

## Why the default changed

`fixtures_factory` now registers an autouse session fixture per layer.
It does nothing but request `{prefix}_session` once, which is enough to park the layer in `keep_for_whole_session` for good.

Isolation is untouched.
`testSetUp` and `testTearDown` still run around every test, so `IntegrationTesting` still aborts the transaction.
What changes is only that the expensive `setUp` stops repeating.

This is the right default because function-style tests are the reason this project exists.
Requiring every consumer to discover the trap and add the fixture themselves would have made a performance cliff the normal experience.

You can opt out with `keep_session=False` — see {doc}`/reference/api`.

## Choosing a scope for your own fixtures

The same economics apply to fixtures you write.

Use **function** scope by default.
It is the safe choice, and for anything cheap the cost is irrelevant.

Reach for **class** scope when setup is expensive and a group of tests can share the result — a REST API suite that needs a portal with content, for example.
Note what you give up: tests in the class are no longer independent, and state leaks from one method to the next.
Sometimes that is exactly what you want, and sometimes it is a bug that only appears when someone runs the tests in a different order.

Use **session** scope for things that are genuinely global and immutable, such as compiling translation files.

`pytest-plone` ships class-scoped `portal_class` and `functional_portal_class` for precisely the middle case.
They carry one caveat worth understanding rather than memorizing: a class-scoped fixture is created once, before any method runs, so it cannot see a marker attached to an individual method.
Only class-level `@pytest.mark.portal` is visible to it.
