"""Tokenizer and tool-document builders for the raw-text retrieval variants.

Tokenization reuses the rules and regexes from task_features so lexical systems
and the feature pass agree on what a word is. Identifiers are split on
snake_case, kebab-case and camelCase before tokenizing.
"""

import re

from toolprune.models import Tool
from toolprune.task_features import ASCII_TOKEN, CJK_RUN, stem

CAMEL_BOUNDARY = re.compile(r"([a-z0-9])([A-Z])")
WORD_OR_CJK = re.compile(f"{ASCII_TOKEN.pattern}|{CJK_RUN.pattern}")
# Function words only. Verbs such as get, find and use stay, because tool names are built from them
# and BM25 already down-weights common terms.
STOPWORDS = frozenset(
    """a an and are as at be but by for from has have i in into is it its me my of on or our
    that the their them there these this to was we were what when where which who will with
    you your""".split()
)
VARIANTS = ("name_desc_server", "name_desc", "desc_only", "name_only", "full")


def tokenize(text: str) -> list[str]:
    """Ordered tokens with duplicates kept. CJK runs become overlapping bigrams."""
    spaced = CAMEL_BOUNDARY.sub(r"\1 \2", text).lower()
    out: list[str] = []
    for match in WORD_OR_CJK.findall(spaced):
        if match[0] in "abcdefghijklmnopqrstuvwxyz0123456789":
            if match not in STOPWORDS and len(match) > 1:
                out.append(stem(match))
        elif len(match) == 1:
            out.append(match)
        else:
            out.extend(match[i:i + 2] for i in range(len(match) - 1))
    return out


def schema_parameters(tool: Tool) -> list[str]:
    props = tool.input_schema.get("properties") or {}
    lines = []
    for pname, spec in props.items():
        desc = (spec or {}).get("description") or ""
        lines.append(f"{pname}: {desc}" if desc else pname)
    return lines


def tool_document(tool: Tool, variant: str = "name_desc_server") -> str:
    if variant == "name_desc_server":
        parts = [tool.name, tool.description, tool.server]
    elif variant == "name_desc":
        parts = [tool.name, tool.description]
    elif variant == "desc_only":
        parts = [tool.description]
    elif variant == "name_only":
        parts = [tool.name]
    elif variant == "full":
        parts = [tool.name, tool.description, tool.server, *schema_parameters(tool)]
    else:
        raise ValueError(f"unknown variant {variant!r}; expected one of {VARIANTS}")
    return "\n".join(p for p in parts if p)
