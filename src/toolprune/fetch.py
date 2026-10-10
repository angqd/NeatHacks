"""Scrape LiveMCPBench raw files from Hugging Face into data/raw and record a manifest."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

BASE = "https://huggingface.co/datasets/ICIP/LiveMCPBench/resolve/main"
FILES = {
    "tools.json": f"{BASE}/tools/tools.json",
    "all_config.json": f"{BASE}/tools/all_config.json",
    "tasks.json": f"{BASE}/tasks/tasks.json",
}


def fetch_raw(raw_dir: Path, force: bool = False) -> dict:
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = raw_dir / "manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest = {}
    with httpx.Client(follow_redirects=True, timeout=120) as client:
        for name, url in FILES.items():
            target = raw_dir / name
            if force or not target.exists():
                resp = client.get(url)
                resp.raise_for_status()
                target.write_bytes(resp.content)
                fetched_at = datetime.now(timezone.utc).isoformat()
            else:
                fetched_at = previous.get(name, {}).get("fetched_at", "unknown")
            data = target.read_bytes()
            manifest[name] = {
                "url": url,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "fetched_at": fetched_at,
            }
    (raw_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest
