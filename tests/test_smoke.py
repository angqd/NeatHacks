import sys

import anthropic
import httpx
import pydantic

import precheck


def test_python_is_312_or_newer():
    assert sys.version_info >= (3, 12)


def test_package_imports_and_versions():
    assert precheck.__version__ == "0.1.0"
    assert pydantic.VERSION
    assert httpx.__version__
    assert anthropic.__version__
