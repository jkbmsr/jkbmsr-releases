#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIRMWARE_DIR = ROOT / "firmware"
LATEST_PATH = FIRMWARE_DIR / "latest.json"
INDEX_PATH = FIRMWARE_DIR / "releases.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_ts(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


def ensure(condition: bool, message: str):
    if not condition:
        raise SystemExit(message)


def main():
    latest = load_json(LATEST_PATH)
    index = load_json(INDEX_PATH)

    ensure(index.get("publicBaseUrl") == "https://cdn.jkbmsr.com", "releases.json must declare https://cdn.jkbmsr.com as publicBaseUrl")
    ensure(isinstance(index.get("releases"), list) and index["releases"], "releases.json must contain at least one release entry")

    releases = index["releases"]
    sorted_releases = sorted(releases, key=lambda item: parse_ts(item["releasedAt"]), reverse=True)
    ensure(releases == sorted_releases, "releases.json must be sorted by releasedAt descending")

    latest_matches = [
        release
        for release in releases
        if release["version"] == latest["currentVersion"] and release["targetHardware"] == latest["targetHardware"]
    ]
    ensure(len(latest_matches) == 1, "latest.json must point to exactly one release entry in releases.json")
    latest_entry = latest_matches[0]
    ensure(latest_entry.get("isLatest") is True, "latest release entry must be marked isLatest=true")
    ensure(latest_entry["releasedAt"] == latest["releasedAt"], "latest release timestamp must match releases.json")

    latest_count = sum(1 for release in releases if release.get("isLatest"))
    ensure(latest_count == 1, "releases.json must contain exactly one isLatest=true entry")

    for release in releases:
      manifest_rel = release["artifacts"]["manifest"]
      manifest_path = FIRMWARE_DIR / manifest_rel.removeprefix("./")
      ensure(manifest_path.exists(), f"missing manifest file: {manifest_rel}")
      manifest = load_json(manifest_path)

      ensure(manifest["version"] == release["version"], f"manifest version mismatch for {manifest_rel}")
      ensure(manifest["targetHardware"] == release["targetHardware"], f"manifest target mismatch for {manifest_rel}")
      ensure(manifest["releasedAt"] == release["releasedAt"], f"manifest release date mismatch for {manifest_rel}")

      for artifact_name, artifact_rel in release["artifacts"].items():
          artifact_path = FIRMWARE_DIR / artifact_rel.removeprefix("./")
          ensure(artifact_path.exists(), f"missing artifact {artifact_name}: {artifact_rel}")

    print("Release index validation passed")


if __name__ == "__main__":
    main()
