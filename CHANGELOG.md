# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0 (2026-05-19)


### New features:

- Added class-scoped portal fixtures `portal_class` and `functional_portal_class`. They share a single Plone Site across every test method in a class and honor `@pytest.mark.portal` when applied at the class level — ideal for REST API and service test suites that need a persistent portal. @ericof [#41](https://github.com/plone/pytest-plone/issues/41)


### Bug fixes:

- Fix CI dependency resolution: `plone-stubs` is now appended to `requirements-mxdev.txt` (with a Python 3.12+ marker) from the Makefile, instead of being declared in `[project.optional-dependencies]` with a `[tool.uv.sources]` git pointer that `uv pip install` ignored. @ericof [#45](https://github.com/plone/pytest-plone/issues/45)


### Internal:

- Update repository URL in package metadata and README to https://github.com/plone/pytest-plone — repository moved from the `collective` organization to `plone`. @ericof 


### Tests

- Test on Plone 6.2 as well, and include Python 3.14.  @mauritsvanrees 

## 1.0.0a3 (2026-04-18)


### New features:

- Added `@pytest.mark.portal` marker support for configuring the `portal` fixture with GenericSetup profiles, pre-created content, and user roles. @ericof [#37](https://github.com/plone/pytest-plone/issues/37)
- Added the `uninstalled` fixture — reads a user-provided `package_name` fixture and calls `installer.uninstall_product`, removing boilerplate from the canonical add-on uninstall smoke test. @ericof [#38](https://github.com/plone/pytest-plone/issues/38)
- Added `functional_app`, `functional_portal`, and `functional_http_request` fixtures — functional-layer counterparts to `app`, `portal`, and `http_request`. `functional_portal` honors the `@pytest.mark.portal` marker. @ericof [#39](https://github.com/plone/pytest-plone/issues/39)
- Added `request_factory`, `manager_request`, and `anon_request` fixtures — build a `RelativeSession` against the functional portal with Manager, Anonymous, or custom basic-auth credentials. Replaces boilerplate duplicated across downstream codebases. @ericof [#40](https://github.com/plone/pytest-plone/issues/40)
- Added `apply_profiles` session-scoped fixture to apply GenericSetup profiles to a Plone site. @ericof 
- Added `create_content` session-scoped fixture to create content items in a Plone site as the site owner. @ericof 
- Added `grant_roles` session-scoped fixture to grant local roles to the test user on a given context. @ericof 


### Internal:

- Updated CI workflows: bumped actions/checkout to v6 and astral-sh/setup-uv to v8.0.0, replaced manual cache with setup-uv built-in caching, fixed Makefile venv creation conflict with setup-uv, and added fail-fast: false to test matrix. @ericof 
- Updated VS Code settings: removed obsolete flake8 config, added plone-stubs to analysis paths. @ericof 
- Updated development tooling: bumped Plone version to 6.1.4, added plone-stubs to test dependencies, updated mx.ini and .gitignore. @ericof 

## 1.0.0a2 (2025-06-11)


### Internal:

- Upgrade zope.pytest to version 8.3. @ericof [#35](https://github.com/plone/pytest-plone/issues/35)
- Fix Makefile release target @ericof 
- Upgrade pytest to version 8.4.0. @ericof 


### Documentation:

- Fix Tests badge on `README.md`. @stevepiercy [#31](https://github.com/plone/pytest-plone/issues/31)

## 1.0.0a1 (2025-03-27)


### Breaking changes:

- Drop support for Python 3.8 @ericof [#17](https://github.com/plone/pytest-plone/issues/17)
- Drop support for Python 3.9 @ericof [#18](https://github.com/plone/pytest-plone/issues/18)


### New features:

- Add support for Python 3.13 @ericof [#19](https://github.com/plone/pytest-plone/issues/19)
- Add support for Plone 6.1 @ericof [#20](https://github.com/plone/pytest-plone/issues/20)
- Add docstring for every fixture provided by pytest-plone @ericof [#24](https://github.com/plone/pytest-plone/issues/24)


### Internal:

- Move from `setuptools` to `hatchling` for package build. @ericof [#21](https://github.com/plone/pytest-plone/issues/21)
- Package metadata now lives in `pyproject.toml`. @ericof [#22](https://github.com/plone/pytest-plone/issues/22)
- Use UV to manage the development environment. @ericof [#23](https://github.com/plone/pytest-plone/issues/23)
- Add default `.vscode` configuration @ericof [#25](https://github.com/plone/pytest-plone/issues/25)
- Add type hints and check codebase with `mypy` [#27](https://github.com/plone/pytest-plone/issues/27)
- Don't reformat `.md` files. @stevepiercy [#28](https://github.com/plone/pytest-plone/issues/28)

## 0.5.0 (2024-05-15)


### New features:

- Add fixture `generate_mo` to compile translation files during tests [@ericof] #5
- Move from `gocept.pytestlayer` to `zope.pytestlayer` [@ericof] #11


### Internal:

- Implement plone/meta [@ericof] #6
- Clean up dependencies for pytest-plone [@thet], [@gforcada], [@ericof] #9
- Pin pytest version to be lower than 8.0 [@ericof] #12
- Update plone/meta [@ericof] #13

## 0.2.0 (2023-01-05)

- Add `app` fixture.
  [ericof]

- Add `setup_tool` and `profile_last_version` fixtures.
  [ericof]

- Add `get_fti` and `get_behaviors` fixtures.
  [ericof]

- Add `get_vocabulary` fixture.
  [ericof]


## 0.1.0 (2023-01-04)

- Fixtures `portal`, `http_request`, `installer`, `browser_layers`, `controlpanel_actions`
  [ericof]

- Initial release
  [ericof]
