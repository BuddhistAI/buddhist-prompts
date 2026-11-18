#!/usr/bin/env python3
"""Regenerate the list of entries in README.md (between the index markers)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import KIND_GROUPS, ROOT, collect_entries  # noqa: E402

START, END = "<!-- index:start -->", "<!-- index:end -->"


def item(e):
    c = e["card"] or {}
    lang = (e["language"] or "any").replace("-", " ").title()
    if e["target"] and e["target"] != "INVALID":
        lang += " → " + e["target"].replace("-", " ").title()
    title = c.get("title") or e["name"]
    where = f"[{title}](./{e['path']}/CARD.md)"
    if c.get("link"):
        where += f" ([source]({c['link']}))"
    summary = f": {c['summary']}" if c.get("summary") else ""
    return f"- {where}{summary} By {c.get('authors', '?')}. {lang}. {c.get('license', '')}".rstrip()


def index():
    entries = collect_entries()
    if not entries:
        return "_Nothing shared yet. Be the first!_"
    by_kind = {}
    for e in entries:
        by_kind.setdefault((e["card"] or {}).get("kind", "other"), []).append(e)
    lines = []
    for kind, heading in KIND_GROUPS:
        if kind in by_kind:
            lines += [f"### {heading}", ""] + [item(e) for e in by_kind[kind]] + [""]
    return "\n".join(lines).rstrip()


def build():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: f"{START}\n{index()}\n{END}", text, flags=re.S)
    return text, new


if __name__ == "__main__":
    _, new = build()
    (ROOT / "README.md").write_text(new, encoding="utf-8")
    print("Wrote the list in README.md")
