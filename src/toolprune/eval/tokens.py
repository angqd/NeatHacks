"""Token counts for tool definitions, using tiktoken o200k_base.

A tool's cost is the count of its JSON definition (name, description, input schema),
serialised with sorted keys so the count does not depend on dict order. This is a proxy
for the model's own tokenizer. Counts are memoized per tool id.
"""

import json
from functools import lru_cache

import tiktoken

from toolprune.models import Tool

ENCODING_NAME = "o200k_base"


@lru_cache(maxsize=1)
def _encoding() -> tiktoken.Encoding:
    return tiktoken.get_encoding(ENCODING_NAME)


def _definition_text(tool: Tool) -> str:
    return json.dumps(
        {"name": tool.name, "description": tool.description, "input_schema": tool.input_schema},
        ensure_ascii=False,
        sort_keys=True,
    )


_counts: dict[str, int] = {}


def tool_tokens(tool: Tool) -> int:
    """Return the number of o200k_base tokens in the tool's definition."""
    if tool.id not in _counts:
        _counts[tool.id] = len(_encoding().encode(_definition_text(tool)))
    return _counts[tool.id]
