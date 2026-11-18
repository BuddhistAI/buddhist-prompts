"""Shared helpers for build.py and check.py. Standard library only."""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGUAGES_URL = "https://raw.githubusercontent.com/BuddhistAI/buddhist-skills/main/languages.json"
# Folders at the top level that are not entries.
NOT_ENTRIES = {"scripts", "templates", "docs"}
# Kind -> the standard file it must have. Other kinds name their file with `file:` in CARD.md.
KIND_FILES = {"skill": "SKILL.md", "workflow": "WORKFLOW.md", "prompt": "PROMPT.md"}
# Catalog order and headings in README.md.
KIND_GROUPS = [
    ("personal", "Personal AI files (CLAUDE.md and similar)"),
    ("project-instructions", "Project instructions"),
    ("style-guide", "Style guides"),
    ("glossary", "Glossaries"),
    ("prompt", "Prompts"),
    ("skill", "Skills (no score yet)"),
    ("workflow", "Workflows"),
    ("other", "Other"),
]
KINDS = {"skill", "workflow", "prompt", "personal", "project-instructions", "style-guide", "glossary", "other"}


def load_languages():
    """Language names come from buddhist-skills languages.json (the one list for all repos)."""
    local = ROOT.parent / "buddhist-skills" / "languages.json"
    if local.exists():
        data = json.loads(local.read_text(encoding="utf-8"))
    else:
        with urllib.request.urlopen(LANGUAGES_URL, timeout=20) as r:
            data = json.load(r)
    return {l["name"]: l for l in data["languages"]}


def parse_frontmatter(path):
    """Return the top-level fields of a CARD.md frontmatter. Flat YAML only."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    return {k: re.sub(r"\s+#.*$", "", v).strip().strip('"') for k, v in re.findall(r"^(\w[\w-]*):[ \t]*(.*)$", m.group(1), re.M)}


def split_name(name, languages):
    """translation-tibetan-to-french -> (translation, tibetan, french); no language -> (name, None, None)."""
    by_len = sorted(languages, key=len, reverse=True)
    target, rest = None, name
    for lang in by_len:
        if rest.endswith(f"-to-{lang}"):
            target, rest = lang, rest[: -len(f"-to-{lang}")]
            break
    for lang in by_len:
        if rest.endswith(f"-{lang}") and len(rest) > len(lang) + 1:
            return rest[: -len(lang) - 1], lang, target
    return name, None, ("INVALID" if target else None)


def collect_entries(languages=None):
    """Entries: <topic>-<language>/<author>-<name>/CARD.md."""
    languages = languages or load_languages()
    entries = []
    for group in sorted(p for p in ROOT.glob("*") if p.is_dir() and not p.name.startswith(".") and p.name not in NOT_ENTRIES):
        topic, lang, target = split_name(group.name, languages)
        for entry in sorted(p for p in group.glob("*") if p.is_dir()):
            card = entry / "CARD.md"
            entries.append({
                "group": group.name,
                "name": entry.name,
                "path": f"{group.name}/{entry.name}",
                "card": parse_frontmatter(card) if card.exists() else None,
                "has_card": card.exists(),
                "topic": topic,
                "language": lang,
                "target": target,
            })
    return entries
