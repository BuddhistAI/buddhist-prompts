#!/usr/bin/env python3
"""Validate every entry's folder and CARD.md, and make sure the README list is current."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import build  # noqa: E402
from lib import KIND_FILES, KINDS, collect_entries  # noqa: E402

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
CARD_FIELDS = ["title", "kind", "topic", "language", "authors", "license", "version", "shared"]

errors = []
entries = collect_entries()
for e in entries:
    where = e["path"]
    if not NAME_RE.match(e["group"]) or not NAME_RE.match(e["name"]):
        errors.append(f"{where}: folder names must be lowercase kebab-case")
    if e["target"] == "INVALID":
        errors.append(f"{where}: '-to-<language>' needs a source language before it, e.g. translation-pali-to-english")
        continue
    if e["language"] is None:
        errors.append(f"{e['group']}: name must end in a language from buddhist-skills languages.json, e.g. style-guide-tibetan or translation-pali-to-english")
    if not e["has_card"]:
        errors.append(f"{where}: missing CARD.md (copy templates/CARD.md)")
        continue
    c = e["card"]
    if c is None:
        errors.append(f"{where}/CARD.md: no frontmatter (see templates/CARD.md)")
        continue
    missing = [k for k in CARD_FIELDS if not c.get(k)]
    if missing:
        errors.append(f"{where}/CARD.md: missing {', '.join(missing)}")
    kind = c.get("kind")
    if kind and kind not in KINDS:
        errors.append(f"{where}/CARD.md: kind must be one of {', '.join(sorted(KINDS))}")
    if c.get("language") and e["language"] and c["language"] != e["language"]:
        errors.append(f"{where}/CARD.md: language {c['language']!r} does not match folder {e['group']!r}")
    if c.get("topic") and e["language"] and c["topic"] != e["topic"]:
        errors.append(f"{where}/CARD.md: topic {c['topic']!r} does not match folder {e['group']!r}")
    if e["target"] and c.get("target-language") != e["target"]:
        errors.append(f"{where}/CARD.md: target-language must be {e['target']!r}")
    if c.get("version") and not SEMVER_RE.match(c["version"]):
        errors.append(f"{where}/CARD.md: version must be semver, e.g. 0.1.0")
    folder = Path(__file__).resolve().parent.parent / where
    if c.get("file"):
        if not (folder / c["file"]).is_file():
            errors.append(f"{where}/CARD.md: file {c['file']!r} is not in this folder")
    elif kind in KIND_FILES:
        if not (folder / KIND_FILES[kind]).is_file():
            errors.append(f"{where}: kind {kind} needs {KIND_FILES[kind]} (or 'file:' in CARD.md)")
    elif kind:
        errors.append(f"{where}/CARD.md: kind {kind} needs 'file:' naming the shared file in this folder")

old, new = build()
if old != new:
    errors.append("README.md list is out of date: run python3 scripts/build.py")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(entries)} entry(ies)")
