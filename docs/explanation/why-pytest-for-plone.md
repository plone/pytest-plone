---
myst:
  html_meta:
    "description": "Why a Plone project that tests with unittest would reach for pytest, and what it costs."
    "property=og:description": "Why a Plone project that tests with unittest would reach for pytest, and what it costs."
    "property=og:title": "About pytest for Plone"
    "keywords": "Plone, pytest, unittest, zope.testrunner, testing"
---

# About pytest for Plone

Plone and Zope test themselves with `unittest`, and they have done so for two decades.
The layer machinery, the test runner, the conventions—all of it grew in that world and works well there.

So why does this package exist?

## What pytest offers

The honest answer is that most of pytest's advantages are small individually and compound into something large.

**Tests are functions.**
No class, no `self`, no inheriting from a base you have to remember the name of.

```python
def test_portal_title(portal):
    assert portal.title == "Plone site"
```

**Fixtures are arguments.**
A test declares what it needs by naming it.
pytest works out what to build, in what order, and when to throw it away.
This replaces `setUp` methods and the inheritance hierarchies they tend to grow.

**Assertions are `assert`.**
`assertEqual`, `assertIn`, `assertGreaterEqual` all collapse into one keyword, and pytest rewrites the expression so the failure output still shows you both sides.

**Parametrization is declarative.**
One decorator turns one test into twenty, each reported separately.

**The ecosystem is large.**
`pytest-xdist` for parallelism, `pytest-cov` for coverage, `pytest-randomly` to shake out order dependencies.

None of these is a reason on its own.
Together they are why pytest became the default in Python, and why Plone developers coming from other projects expect it.

## What it costs

Being straightforward about the trade-offs:

**Another layer of machinery.**
`pytest-plone` sits on `zope.pytestlayer`, which sits on `plone.testing`. When something breaks, the stack you have to understand is deeper.

**The layer model does not map cleanly onto pytest.**
Layers and pytest fixtures are two different answers to the same question, and bolting them together has sharp edges. The session-scoping trap described in {doc}`layers-scopes-and-isolation` is a direct consequence of that mismatch.

**Core does not use it.**
Plone core is tested with `zope.testrunner`. If you are contributing to core, you still need to know that world.

## The pragmatic position

`pytest-plone` does not ask you to abandon the layers.
It reuses them.

Your `plone.testing` layers stay exactly as they are; `fixtures_factory` turns them into pytest fixtures, and your tests become functions that ask for a `portal`.
The expensive, well-tested Plone setup machinery is untouched; only the way tests are written and run changes.

That is the bet this package makes: keep what Plone got right about test setup, and drop what `unittest` got tedious about test authoring.
