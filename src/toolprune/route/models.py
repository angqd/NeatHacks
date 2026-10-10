"""Output contracts for the three routing stages. Names and ids are enums built from the loaded
groups and tools, so the model cannot return a group or tool that does not exist."""

from typing import Literal

from pydantic import BaseModel, create_model

ROUTER_VERSION = "route-v1"
MAX_GROUPS_PER_CAPABILITY = 2
MAX_TOOLS_PER_CAPABILITY = 4


def plan_model(group_names: list[str]) -> type[BaseModel]:
    """Stage 1 output: the capabilities the request needs, each with its best groups."""
    group_type = Literal[tuple(group_names)]  # type: ignore[valid-type]
    capability = create_model("Capability", need=(str, ...), groups=(list[group_type], ...))  # type: ignore[valid-type]
    return create_model("CapabilityPlan", capabilities=(list[capability], ...))  # type: ignore[valid-type]


def selection_model(tool_ids: list[str]) -> type[BaseModel]:
    """Stage 2 and 3 output: for each capability, the chosen tools and whether it is covered."""
    tool_type = Literal[tuple(tool_ids)]  # type: ignore[valid-type]
    entry = create_model(
        "CapabilityChoice",
        need=(str, ...),
        tool_ids=(list[tool_type], ...),  # type: ignore[valid-type]
        covered=(bool, ...),
    )
    return create_model("Selection", choices=(list[entry], ...))  # type: ignore[valid-type]
