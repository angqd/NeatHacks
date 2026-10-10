"""Data contracts for the enricher.

Pass 1 writes every tag field except the final `domain`. It writes a free-form `topic`
instead; the grouper later induces a taxonomy from the topics and assigns `domain` from it.
Fields copied from the source (tool_id, server, name) are never written by the model.
"""

from typing import Literal

from pydantic import BaseModel, Field

PROMPT_VERSION = "pass1-v2"

Effect = Literal["read", "write", "destructive"]
Flag = Literal["instruction_like_text", "ambiguous_purpose", "missing_description"]
ModelFlag = Literal["instruction_like_text", "ambiguous_purpose"]

SUMMARY_MAX_WORDS = 25
INTENT_MAX_WORDS = 12
INTENTS_MIN, INTENTS_MAX = 2, 3
SERVER_SUMMARY_MAX_WORDS = 30


class ToolTagDraft(BaseModel):
    """What the model writes for one tool."""

    name: str = Field(description="The exact tool name as given.")
    topic: str = Field(description="Lowercase snake_case label of 1 to 3 words for the kind of task.")
    summary: str
    intents: list[str]
    effect: Effect
    flags: list[ModelFlag]


class ServerEnrichment(BaseModel):
    """What the model writes for one server: one entry per tool, in the given order."""

    server_summary: str
    tools: list[ToolTagDraft]


class ToolTag(BaseModel):
    """One stored tag. `domain` is None until the grouper assigns it."""

    tool_id: str
    server: str
    name: str
    domain: str | None = None
    topic: str
    summary: str
    intents: list[str]
    effect: Effect
    flags: list[Flag]
    effect_source: Literal["model", "source_annotation"]
    doc_hash: str
    model: str
    prompt_version: str = PROMPT_VERSION


class ServerCard(BaseModel):
    server: str
    server_summary: str
    n_tools: int
    model: str
    prompt_version: str = PROMPT_VERSION


def word_count(text: str) -> int:
    return len(text.split())


def check_draft(draft: ServerEnrichment, expected_names: list[str]) -> list[str]:
    """Return a list of violations. Empty means the draft is acceptable."""
    problems: list[str] = []
    got = [t.name for t in draft.tools]
    if got != expected_names:
        problems.append(f"tool names must match the input exactly and in order; expected {expected_names}, got {got}")
    if word_count(draft.server_summary) > SERVER_SUMMARY_MAX_WORDS:
        problems.append(f"server_summary has more than {SERVER_SUMMARY_MAX_WORDS} words")
    for t in draft.tools:
        if word_count(t.summary) > SUMMARY_MAX_WORDS:
            problems.append(f"{t.name}: summary has more than {SUMMARY_MAX_WORDS} words")
        if not INTENTS_MIN <= len(t.intents) <= INTENTS_MAX:
            problems.append(f"{t.name}: intents must hold {INTENTS_MIN} to {INTENTS_MAX} items")
        for i in t.intents:
            if word_count(i) > INTENT_MAX_WORDS:
                problems.append(f"{t.name}: an intent has more than {INTENT_MAX_WORDS} words")
        if not t.topic or t.topic != t.topic.lower() or " " in t.topic:
            problems.append(f"{t.name}: topic must be lowercase snake_case with no spaces")
    return problems
