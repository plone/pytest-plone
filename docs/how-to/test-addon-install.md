# How to test that your add-on installs and uninstalls

This guide shows you how to write the canonical setup suite for a Plone add-on: the add-on installs, brings its pieces with it, and removes them again cleanly.

It assumes you have a `package_name` fixture — see {doc}`set-up-pytest-plone`.

## Check the product is installed

```python
def test_product_installed(installer, package_name):
    assert installer.is_product_installed(package_name) is True
```

## Check the browser layer is registered

```python
def test_browserlayer(browser_layers):
    from my.addon.interfaces import IMyAddonLayer

    assert IMyAddonLayer in browser_layers
```

## Check the profile version

```python
def test_profile_version(profile_last_version, package_name):
    assert profile_last_version(f"{package_name}:default") == "1000"
```

## Check the control panel is there

```python
def test_controlpanel_installed(controlpanel_actions):
    assert "my-addon-controlpanel" in controlpanel_actions
```

## Check the content type is registered

```python
import pytest


@pytest.mark.parametrize(
    "behavior",
    [
        "plone.dublincore",
        "plone.namefromtitle",
        "plone.shortname",
    ],
)
def test_has_behavior(get_behaviors, behavior):
    assert behavior in get_behaviors("Person")
```

## Check it uninstalls

The [`uninstalled`](/reference/fixtures.md#add-ons) fixture uninstalls the add-on for you.
Pull it in with `usefixtures` so it runs before every test in the class:

```python
import pytest


@pytest.mark.usefixtures("uninstalled")
class TestUninstall:
    def test_product_uninstalled(self, installer, package_name):
        assert installer.is_product_installed(package_name) is False

    def test_browserlayer_removed(self, browser_layers):
        from my.addon.interfaces import IMyAddonLayer

        assert IMyAddonLayer not in browser_layers
```

The uninstall check is the one developers most often skip, and it is the one that catches profiles that add things without removing them.
