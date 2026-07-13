"""Guard the ``python`` code examples embedded in our docstrings.

These examples are the package's most-copied documentation, and they become the
single source of truth once an autodoc-generated API reference renders them.
Nothing executes them, so errors survive indefinitely unless we check them here.

Both checks are pure AST work -- no Plone layer, no fixtures, milliseconds.
"""

from pathlib import Path

import ast
import pytest
import pytest_plone
import re
import textwrap


PYTHON_FENCE = re.compile(r"```python\n(.*?)```", re.S)

DOCSTRING_NODES = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)

PACKAGE_ROOT = Path(pytest_plone.__file__).parent


def iter_examples():
    """Yield (source_file, owner, code) for every ```python``` block in a docstring."""
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node, DOCSTRING_NODES):
                continue
            docstring = ast.get_docstring(node)
            if not docstring:
                continue
            owner = getattr(node, "name", "<module>")
            for block in PYTHON_FENCE.findall(docstring):
                yield path.name, owner, textwrap.dedent(block)


EXAMPLES = list(iter_examples())

IDS = [f"{filename}::{owner}" for filename, owner, _ in EXAMPLES]


def test_examples_found():
    """Guard the guard: a broken extractor must not silently pass everything."""
    assert len(EXAMPLES) > 20


@pytest.mark.parametrize(("filename", "owner", "code"), EXAMPLES, ids=IDS)
def test_example_is_valid_python(filename: str, owner: str, code: str):
    """Every embedded example must parse.

    Catches truncated snippets and unterminated string literals.
    """
    try:
        ast.parse(code)
    except SyntaxError as exc:  # pragma: no cover - failure path
        pytest.fail(f"{filename}::{owner} example is not valid Python: {exc.msg}")


@pytest.mark.parametrize(("filename", "owner", "code"), EXAMPLES, ids=IDS)
def test_example_has_no_self_in_plain_test(filename: str, owner: str, code: str):
    """A module-level ``def test_x(self, ...)`` is always wrong.

    pytest resolves every parameter as a fixture, so a stray ``self`` outside a
    class fails with ``fixture 'self' not found``. Methods inside a ``class
    Test...`` are unaffected -- only top-level functions are checked.
    """
    for statement in ast.parse(code).body:
        if not isinstance(statement, ast.FunctionDef):
            continue
        arguments = [argument.arg for argument in statement.args.args]
        assert "self" not in arguments, (
            f"{filename}::{owner}: top-level `def {statement.name}("
            f"{', '.join(arguments)})` takes `self` outside a class; "
            "pytest will fail with \"fixture 'self' not found\""
        )
