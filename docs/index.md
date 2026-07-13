---
myst:
  html_meta:
    "description": "pytest-plone provides pytest fixtures and helpers to test Plone add-ons."
    "property=og:description": "pytest-plone provides pytest fixtures and helpers to test Plone add-ons."
    "property=og:title": "pytest-plone"
    "keywords": "Plone, pytest, testing, fixtures, add-ons"
---

# `pytest-plone`

`pytest-plone` is a [pytest](https://docs.pytest.org/en/stable/) plugin that provides fixtures and helpers to test [Plone](https://plone.org) add-ons.

It builds on [zope.pytestlayer](https://github.com/zopefoundation/zope.pytestlayer), turning the `plone.testing` layers you already have into pytest fixtures.
You write plain function-style tests, and the Plone site arrives as an argument.

```python
def test_portal_title(portal):
    assert portal.title == "Plone site"
```

## Where to go next

`````{grid} 1 1 2 2
:gutter: 3

````{grid-item-card} Tutorial
:link: tutorials/first-test
:link-type: doc

New to `pytest-plone`?
Write your first test for an add-on, start to finish.
````

````{grid-item-card} How-to guides
:link: how-to/index
:link-type: doc

Solve a specific problem: set the plugin up, test an add-on install, speed up a slow suite.
````

````{grid-item-card} Reference
:link: reference/index
:link-type: doc

Look something up: every fixture, every marker, the `fixtures_factory` API.
````

````{grid-item-card} Explanation
:link: explanation/index
:link-type: doc

Understand the machinery: testing layers, fixture scopes, and how isolation works.
````
`````

```{toctree}
:hidden:
:maxdepth: 2

tutorials/first-test
how-to/index
reference/index
explanation/index
```
