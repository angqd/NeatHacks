import sys
from importlib.metadata import version

import agents
import httpx
import pydantic

import toolprune


def test_python_is_312_or_newer():
    assert sys.version_info >= (3, 12)


def test_package_imports_and_versions():
    assert toolprune.__version__ == "0.1.0"
    assert pydantic.VERSION
    assert httpx.__version__
    assert version("openai-agents")
    assert agents.Agent is not None
