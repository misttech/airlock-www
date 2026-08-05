# AGENTS.md

Operating guide for humans and AI coding agents working in **airlock-www**.

> **What this is:** the public website for Airlock, published to GitHub Pages.
> It is HTML and CSS, served exactly as written.

## Settled decisions (do not relitigate)

- **No build step.** No static site generator, no bundler, no npm. The page is
  reviewable in a diff and cannot break because a toolchain moved underneath
  it. A generator would need a written justification, not a preference — and
  the site is one page.
- **No external origin.** No CDN font, script, tracker, analytics, or embed.
  Every asset is committed and served from this repository. The page observes
  nobody, and that is a property to keep deliberately rather than lose to a
  convenient embed. `make check` enforces it.
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

## The beta form is a mailto

There is no server here, so a form cannot POST anywhere. The alternatives were
a third-party form service — a dependency, and a processor holding other
people's email addresses — or `mailto:`. `mailto:` matches how the rest of the
project is built: no external service, nothing stored, and the sender's own
address arrives with the request, which is the point of the signup.

The script only prefills the message body. With JavaScript disabled the plain
link still works and the address is printed in full to be copied, so **any
change here must keep working without JavaScript**.

**A `mailto:` is not enough on its own.** It does something only for a visitor
whose browser has a mail client registered as its handler — being signed into
webmail in another tab is not that, and the click silently does nothing. A
browser cannot report whether a `mailto:` was handled, so there is no failure to
detect and nothing to fall back *to* after the fact. Submitting therefore
attempts the `mailto:` and reveals the composed message as copyable text in the
same gesture. That covers every mail setup without guessing which webmail the
visitor uses, and without the external origin a Gmail or Outlook compose link
would put on a page that has none. `make check` enforces that both halves stay.

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
