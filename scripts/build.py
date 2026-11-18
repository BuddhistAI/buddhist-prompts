#!/usr/bin/env python3
"""Regenerate the list of entries in README.md (between the index markers)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ROOT, collect_entries  # noqa: E402

LABELS = {"skill": "Skill", "workflow": "Workflow", "prompt": "Prompt", "personal": "Personal AI file",
          "project-instructions": "Project instructions", "style-guide": "Style guide", "glossary": "Glossary", "other": "Other"}
START, END = "<!-- index:start -->", "<!-- index:end -->"


def index():
    entries = collect_entries()
    if not entries:
        return "_Nothing shared yet. Be the first!_"
    lines = ["| Entry | Kind | Language | Topic | By | Version |", "| --- | --- | --- | --- | --- | --- |"]
    for e in entries:
        c = e["card"] or {}
        lang = (e["language"] or "any").replace("-", " ").title()
        if e["target"] and e["target"] != "INVALID":
            lang += " → " + e["target"].replace("-", " ").title()
        lines.append(f"| [{c.get('title') or e['name']}](./{e['path']}/CARD.md) | {LABELS.get(c.get('kind', ''), c.get('kind', ''))} | {lang} | {e['topic']} | {c.get('authors', '')} | {c.get('version', '')} |")
    return "\n".join(lines)


def build():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: f"{START}\n{index()}\n{END}", text, flags=re.S)
    return text, new


if __name__ == "__main__":
    _, new = build()
    (ROOT / "README.md").write_text(new, encoding="utf-8")
    print("Wrote the list in README.md")
