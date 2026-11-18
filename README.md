# Buddhist prompt library

**Files that people give to AI for Buddhist work, shared so others can learn from them and use them.** Also skills and workflows that have no score yet.

This is the place to share any part of your AI setup:

- your `CLAUDE.md` or other personal AI file
- project instructions for a translation or study project
- a style guide, for example how your teacher speaks
- a glossary
- a prompt you paste into a chat assistant
- a skill or workflow that has no benchmark yet

Nothing here has a score. When a task has a benchmark, its skills are measured in the task's workshop repo (for example [toc-extraction-tibetan](https://github.com/BuddhistAI/toc-extraction-tibetan)), and the best ones are released in [buddhist-skills](https://github.com/BuddhistAI/buddhist-skills). Part of [BuddhistAI](https://buddhistai.github.io/).

## Share yours

**No git needed:** open the [Share your files](https://github.com/BuddhistAI/buddhist-prompt-library/issues/new?template=share.yml) form. Paste a link, or drag your files into the form. You need a free GitHub account ([make one](https://github.com/signup)). Your name and picture are optional.

**The form is public at once**, before anyone reviews it. Do not upload private or restricted material.

A maintainer adds your entry here and credits you on the [contributors list](https://buddhistai.github.io/#people). GitHub sends you a message when it is added. Is it a skill for a task that has a benchmark? A maintainer also adds it to that task's repo so it can be scored, with your name.

**With a pull request:** copy `templates/CARD.md` into a new folder and add your file (see the layout below). Run `python3 scripts/build.py` and `python3 scripts/check.py`. If you cannot, say so in the pull request and a maintainer will.

Only share material you are free to share: no texts with restricted transmission, and no copyrighted translations without permission. See the [code of conduct](./CODE_OF_CONDUCT.md).

## Use an entry

Open its `CARD.md`: it says what the file is and how to use it. Then open the file itself and copy all its text.

- **In Claude.ai:** paste it into a Project's instructions.
- **In ChatGPT:** paste it into a GPT's instructions, or at the start of a chat.
- **In Claude Code on your computer:** a `CLAUDE.md` goes in your project folder, and a skill folder goes in `~/.claude/skills/`.

Tell the author how it went, in [Discussions](https://github.com/orgs/BuddhistAI/discussions) or an issue.

## All entries

<!-- index:start -->
| Entry | Kind | Language | Topic | By | Version |
| --- | --- | --- | --- | --- | --- |
| [my-dharma.md (Shoukei Matsumoto's version)](./personal-ai-setup-english/shoukei-matsumoto-my-dharma/CARD.md) | Personal AI file | English | personal-ai-setup | Shoukei Matsumoto | 1.0.0 |
<!-- index:end -->

## Layout

```
<topic>-<language>/<author>-<short-name>/
  CARD.md        what it is, who made it, how to use it (from templates/CARD.md)
  <the file>     SKILL.md, WORKFLOW.md, PROMPT.md, or any file name (set file: in CARD.md)
  SOURCE.md      where it came from, the author, the date and the license
```

- `<topic>`: for a skill or workflow, a task ID from [tasks/index.json](https://github.com/BuddhistAI/buddhist-benchmarks/blob/main/tasks/index.json) when one fits, so it can be measured later. For other kinds, a short name in lowercase with hyphens: `personal-ai-setup`, `style-guide`, `glossary`.
- `<language>`: the Buddhist language the file is for, a full name from buddhist-skills [languages.json](https://github.com/BuddhistAI/buddhist-skills/blob/main/languages.json) (for example `tibetan`, `pali`). If it is for no one language, the language it is written in (for example `english`). Translation adds `-to-<language>`: `translation-pali-to-english`. One language per entry.
- `kind` in CARD.md is one of: `skill`, `workflow`, `prompt`, `personal` (a personal AI file), `project-instructions`, `style-guide`, `glossary`, `other`.
- CARD.md fields: `title`, `kind`, `file` (needed for kinds other than skill, workflow and prompt), `topic`, `language`, `target-language` (translation only), `authors`, `github`, `avatar`, `contact`, `license`, `version`, `shared`.

## For maintainers: turn a Share issue into an entry

1. Make the folder `<topic>-<language>/<author>-<short-name>/` and copy the files from the link or the issue attachments, unchanged.
2. Write `CARD.md` from the issue. Set `kind`, `file`, `authors` (the name they gave, or their GitHub name), `github` (the issue author, unless they ask not to be shown), `avatar` (the picture they attached, if any) and `license` (their choice).
3. Write `SOURCE.md`: the issue or repo link, the author, the date and the license. Files under a license other than MIT keep that license.
4. Run `python3 scripts/build.py` and `python3 scripts/check.py`, open the pull request with `Closes #<issue>`, and thank the author in the issue.

The daily contributors job on the homepage reads `authors`, `github` and `avatar` from every `CARD.md` here, so the author appears in the contributors list after the merge.

If a shared skill is for a task that has a benchmark, also copy it as a variant into that task's repo (for example [toc-extraction-tibetan](https://github.com/BuddhistAI/toc-extraction-tibetan)) so it can be measured.

## License

MIT, unless an entry says otherwise in its `CARD.md` and `SOURCE.md`.
