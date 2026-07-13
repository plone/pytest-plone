---
myst:
  html_meta:
    "description": "Background on pytest for Plone, and on how testing layers, scopes, and isolation fit together."
    "property=og:description": "Background on pytest for Plone, and on how testing layers, scopes, and isolation fit together."
    "property=og:title": "pytest-plone explanation"
    "keywords": "Plone, pytest, testing layers, isolation"
---

# Explanation

Background and reasoning.
Read these away from the keyboard.

{doc}`why-pytest-for-plone`
:   Why a project whose core tests with `unittest` would reach for pytest, and what that costs.

{doc}`layers-scopes-and-isolation`
:   What a testing layer is, how it becomes a pytest fixture, how isolation really works — and the performance trap that lurks in the seam between the two models.

```{toctree}
:hidden:
:maxdepth: 2

why-pytest-for-plone
layers-scopes-and-isolation
```
