"""Render the historical standalone config; --check detects stale copies in CI."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "esphome config 10-8-2023.yaml"
INCLUDE = "packages:\n  deye: !include packages/deye.yaml\n"
HEADER = (
    "# Generated from deye.yaml and packages/deye.yaml; do not edit in the repository.\n"
    "# Regenerate with: python scripts/sync_legacy.py\n"
    "# This standalone copy is retained for existing links and manual installations.\n\n"
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    entry = (ROOT / "deye.yaml").read_text(encoding="utf-8")
    if entry.count(INCLUDE) != 1:
        raise SystemExit("Expected exactly one local Deye package include in deye.yaml")
    package = (ROOT / "packages/deye.yaml").read_text(encoding="utf-8")
    rendered = HEADER + entry.replace(INCLUDE, package)
    if args.check:
        if not LEGACY.exists() or LEGACY.read_text(encoding="utf-8") != rendered:
            raise SystemExit("Standalone config is stale: run python scripts/sync_legacy.py")
        print("Standalone config matches the package sources.")
    else:
        LEGACY.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"Updated {LEGACY.name}")


if __name__ == "__main__":
    main()
