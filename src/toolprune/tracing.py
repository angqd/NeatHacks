"""neatlogs tracing setup shared by all ToolPrune workflows.

init_tracing() loads the repo .env, then initialises neatlogs with the OpenAI
SDK and OpenAI Agents SDK instrumentations. It is idempotent and never raises.
Without NEATLOGS_API_KEY it logs one warning and returns False.

Run the end-to-end check with: python -m toolprune.tracing
"""

import logging
import os

from toolprune.env import load_env

logger = logging.getLogger(__name__)

INSTRUMENTATIONS = ["openai", "openai_agents"]
CHECK_WORKFLOW = "tool-retrieval-eval"
CHECK_MODEL = "text-embedding-3-small"

_initialized = False


def init_tracing(workflow_name: str) -> bool:
    """Initialise neatlogs for one workflow. Returns True when tracing is on."""
    global _initialized
    if _initialized:
        return True

    load_env()
    if not os.getenv("NEATLOGS_API_KEY", "").strip():
        logger.warning("NEATLOGS_API_KEY is not set; tracing is disabled.")
        return False

    try:
        import neatlogs

        neatlogs.init(
            workflow_name=workflow_name,
            instrumentations=INSTRUMENTATIONS,
        )
    except Exception as exc:  # tracing must never break a run
        logger.warning("neatlogs initialisation failed: %s", exc)
        return False

    _initialized = True
    return True


def _check() -> None:
    from openai import OpenAI

    tracing_on = init_tracing(CHECK_WORKFLOW)
    load_env()
    client = OpenAI()
    resp = client.embeddings.create(model=CHECK_MODEL, input="hello")
    print(f"embedding length: {len(resp.data[0].embedding)}")
    print(f"tracing initialised: {tracing_on}")

    if tracing_on:
        import neatlogs

        neatlogs.flush()
        neatlogs.shutdown()


if __name__ == "__main__":
    _check()
