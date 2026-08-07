# Commit message style guide

The same conventions as [airlock](https://github.com/misttech/airlock), so the
repositories read as one history. This file records the differences, which are
few — this repository is one page.

## Subject line

`[component] Imperative summary`, under 50 characters where it fits.

Imperative, as though completing "this change will…": *Show the dashboard*, not
*Showed* or *Showing*.

## Component tags {#component-tags}

| tag | area |
|---|---|
| `[page]` | `index.html`, `invite/index.html` — content and structure |
| `[style]` | `assets/style.css` — the design system |
| `[assets]` | fonts, screenshots, anything binary |
| `[docs]` | `README.md`, `AGENTS.md`, this guide |
| `[build]` | `Makefile`, `scripts/`, the Pages workflow |
| `[repo]` | repo meta: `.gitignore`, `.editorconfig`, licence, editor config |

A change small enough to touch only one file usually needs only one tag. If it
needs four, it is probably several commits.

## Body

Separate from the subject with a blank line. Wrap at 72 characters.

Explain the *reason*. On a marketing page the reason is usually about a claim —
what it now says, what it stopped saying, and why that is more accurate rather
than merely shorter.

A body is worth writing whenever a change touches something AGENTS.md calls
settled: the absence of a build step, the absence of external origins, the rule
that no link points into a private repository, or the requirement that claims
match the project's documentation. A commit that erodes one of those should say
so out loud rather than leave a reader to discover it.

## Footers

- **`Bug:`** — `Fixes #n` / `Closes #n` to auto-close, `Refs #n` to link.
  Optional; use it whenever an issue exists.
- **`Test:`** — how the change was verified, when it is not obvious. For this
  repository that usually means which viewport widths and which colour scheme
  you actually looked at, since `make check` covers structure and nothing else.

Every commit ends with:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

## Pull requests

The subject and body rules apply unchanged to a PR title and description — this
repository merges by rebase, so a sloppy PR title becomes permanent history.

`.github/pull_request_template.md` prefills what a reviewer here needs. Delete
sections that do not apply; a heading with nothing under it tells a reviewer
less than its absence does.
