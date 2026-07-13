---
myst:
  html_meta:
    "description": "Practical guides for testing Plone add-ons with pytest-plone."
    "property=og:description": "Practical guides for testing Plone add-ons with pytest-plone."
    "property=og:title": "pytest-plone how-to guides"
    "keywords": "Plone, pytest, how-to, add-on, REST API, performance"
---

# How-to guides

Practical recipes for people who already know what they want.

{doc}`set-up-pytest-plone`
:   Add the plugin to an existing add-on and write your `conftest.py`.

{doc}`test-addon-install`
:   The canonical setup suite: the add-on installs, brings its pieces, and removes them again.

{doc}`test-a-rest-api`
:   Drive a `plone.restapi` service with real HTTP requests.

{doc}`speed-up-the-test-suite`
:   Diagnose a slow suite and fix it.

```{toctree}
:hidden:
:maxdepth: 2

set-up-pytest-plone
test-addon-install
test-a-rest-api
speed-up-the-test-suite
```
