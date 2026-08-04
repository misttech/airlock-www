<!--
Title: an imperative summary, same form as a commit subject.

Every commit ends with:
  Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

Delete any section that does not apply. An honestly deleted section is more
useful than a heading with nothing under it.
-->

## Summary

<!--
One paragraph: what this changes and why it needed changing. If the branch is
several commits, say how they are scoped — a reader should know whether to
review the branch as one change or commit by commit.
-->

## What changed

<!--
Group by the area or boundary touched, in bold. Lead with the problem, then the
fix — "X was possible because Y; now Z" reads far better than "added a check in
Z", and it lets a reviewer disagree with the premise rather than only the code.

Name interfaces and boundaries, not every file; the diff already lists files.
-->

## ⚠️ Breaking changes

<!--
Anything an existing deployment must do differently: changed defaults, newly
required flags, a config that will now refuse to start, a migration.

Say *why* it changed, not just what — "an empty audience accepted tokens minted
for any client at that issuer" tells an operator whether they were exposed.

Record each one in docs/upgrading.md in this same PR and link it here.

Also worth a line: behaviour that is not breaking but is not what a reader
would assume — e.g. protection that only lands per-VM on next boot rather than
at upgrade time.
-->

## Test plan

<!--
Commands you actually ran, with results. "Tests pass" is not checkable;
"18 packages pass" and "45 Rust tests, clippy clean" are.
-->

```
python3 -m http.server 8000    # then open it and read the page
```

- [ ] Looked at the rendered page, not just the diff
- [ ] Checked light **and** dark
- [ ] Checked a narrow viewport
- [ ] Every link resolves for a logged-out visitor

**New coverage:** <!-- what the added tests actually pin down -->

## Site rules

- [ ] **No build step** — still plain HTML and CSS, served as written. A
      generator or bundler needs a written justification, not a preference.
- [ ] **No external origin** — no CDN font, script, tracker, analytics, or
      embed. Assets are committed and served from this repository.
- [ ] **No link to a private repository** — the site is public and the code is
      not; a link a visitor cannot open is worse than no link.
- [ ] **Claims match the documentation** — every statement is drawn from the
      Airlock README and docs. This page must never oversell what tenant
      isolation actually covers.
- [ ] **The status notice still says the project is early** and is still near
      the top, not buried.
- [ ] **Renders in both light and dark**, and at a narrow width.

## Privacy

<!--
Delete only if the change genuinely touches none of this.

- Does it introduce anything that observes a visitor — a script, a pixel, an
  external font, an embed? The page does none of that today. That is a property
  worth keeping deliberately rather than losing by accident.
- Does it collect an address or other personal data? Where does it go, and who
  ends up holding it?
- Does it publish an address a scraper will harvest?
-->

## Note for reviewers

<!--
Where a mistake here is expensive. On a public page that is usually a claim:
something stated more confidently than the documentation supports, or a
capability implied that does not exist yet.

Also the place for anything you found but deliberately did not fix, so it stays
a decision rather than a surprise for whoever reads it next.
-->

---

Bug: <!-- Fixes #n / Closes #n to auto-close, Refs #n to link. Delete if none. -->
Test: <!-- one line, when the test plan above is not self-evident -->
