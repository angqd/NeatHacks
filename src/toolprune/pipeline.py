"""Download the LiveMCPBench files as published, with a manifest. No normalization or annotation.

Run: python -m toolprune.pipeline [--force]
"""

import json
import sys
from pathlib import Path

from toolprune import fetch

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"


def main() -> None:
    manifest = fetch.fetch_raw(RAW_DIR, force="--force" in sys.argv)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
