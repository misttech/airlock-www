# AGENTS.md

Operating guide for humans and AI coding agents working in **airlock-www**.

> **What this is:** the public website for Airlock, published to GitHub Pages.
> It is HTML and CSS, served exactly as written.

## Settled decisions (do not relitigate)

- **No build step.** No static site generator, no bundler, no npm. The page is
  reviewable in a diff and cannot break because a toolchain moved underneath
  it. A generator would need a written justification, not a preference — and
  the site is one page.
- **Nothing is loaded from another origin.** No CDN font, script, tracker,
  analytics, or embed. Every asset is committed and served from this
  repository, so the page observes nobody — a property to keep deliberately
  rather than lose to a convenient embed.

  **One origin is written to**, and only one: the beta form posts to its
  endpoint when a visitor clicks the button. Never on load, never anything
  else. `make check` enforces the two halves separately, because they are
  different rules — a form action is somewhere a visitor chose to send their
  own address, and a CDN font is a third party watching everyone who reads the
  page. Adding a *second* endpoint, or any load, needs a written justification.
- **This repository is public; the code repositories are not.** That asymmetry
  is the reason the site lives here at all — GitHub Pages on a free plan
  requires a public repository, and putting the site in `airlock` would have
  forced the code public too. It also means **no link may point into a private
  repository**: a link a visitor cannot open is worse than no link.
- **Claims come from the Airlock README and docs.** If a statement here outruns
  what those say, the page is wrong. This matters most around tenant isolation,
  which the project documents honestly and this page must not oversell.
- **One colour.** The stylesheet is the design system the dashboard uses,
  adapted from [The Monospace Web](https://github.com/owickstrom/the-monospace-web)
  (MIT). Everything lands on a character grid. Colour is not decoration.

## The domain

The site is served at `airlock.mist-os.com`, which is what the `CNAME` file at
the root declares. It is committed rather than left to the repository setting
because publishing goes through a workflow: the deployed artifact is the whole
tree, so the domain travels with the deploy and is visible in a diff like
everything else here.

Every path on the site is relative for the same reason it always was — it makes
the tree serveable from any prefix, which is what let the domain change without
touching a page.

## Pages

Two: `index.html`, and `invite/index.html` which is the beta form on a page of
its own. The form used to sit near the top of the home page, which put four
fields in front of a reader before the page had said what the thing was. Its own
page also gives the call to action somewhere to point — the bar's button, and
the one under the lede — instead of scrolling.

`scripts/check.py` applies the structural rules to both, and **finds** the form
rather than assuming which page holds it, so moving it again cannot quietly drop
its guarantees from the check.

## The beta form

It posts to a Google Form's `formResponse` URL —
[`docs/beta-form.md`](docs/beta-form.md) is the wiring.

It was a `mailto:` first. That failed for a larger group than expected: a
`mailto:` does something only for a visitor whose browser has a mail client
registered as its handler, and being signed into webmail in another tab is not
that. The click silently does nothing, and a browser cannot report that it did
nothing, so there was no failure to detect and nothing to fall back *to*.

A third-party form service was rejected — a company holding other people's
email addresses. **An Apps Script web app was written and then rejected too**,
which is the more useful thing to record: its consent screen asks for *all your
spreadsheets* and *send email as you*, permanently, so that a signup box works.
A Form grants nothing at all. There is no OAuth screen, nothing deployed, and no
code of ours executing as anybody.

The trade that buys: `formResponse` is undocumented. It has worked for over a
decade and every custom-front-end-for-Forms guide leans on it, but Google never
promised it, and a cross-origin POST is opaque so the page cannot notice if it
breaks. Hence the printed address, and hence checking the form for real after
touching it.

Three properties hold this together, and **a change here must keep all three**:

- **It works with JavaScript disabled.** The form is a real `method="post"`; the
  browser navigates to the endpoint and the endpoint answers with a page. The
  script only upgrades that to an inline confirmation.
- **A failed submit is never silent.** A cross-origin POST is opaque, so the
  page cannot read the reply. A request that never left reveals a copyable
  message instead — the same escape hatch the whole form degrades to if the
  endpoint is ever retired.
- **The address stays printed in full.** It is the way in that depends on
  nothing at all.

`make check` enforces each one.

## Working on it

```sh
make serve     # http://localhost:8000
make check     # HTML well-formedness, external origins, private-repo links
```

Then **look at the page** — in both light and dark, and at a narrow width. The
checks catch structure, not layout.

## Screenshots

Screenshots are of a real fleet on a live control plane, never mockups, and
they are captured in both themes because the page follows the reader's colour
scheme. Regenerate both when the dashboard's appearance changes materially;
a stale screenshot is a claim that has quietly stopped being true.

## Commit and PR conventions

[`docs/contribute/commit-message-style-guide.md`](docs/contribute/commit-message-style-guide.md).
`.github/pull_request_template.md` prefills a PR description.

Every commit ends with:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```
