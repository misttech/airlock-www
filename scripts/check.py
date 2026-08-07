#!/usr/bin/env python3
# Copyright 2026 Mist Tecnologia LTDA. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Check the site's structural invariants.

These are the rules from AGENTS.md that a machine can actually verify, so they
stop depending on a reviewer remembering them. Layout is not checked — for that
you have to open the page and look.
"""

import html.parser
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Every page on the site. The structural rules apply to all of them; the beta
# form's rules apply to whichever one carries the form, which is why that is
# found rather than assumed — moving the form to its own page must not quietly
# take its guarantees out of the check.
PAGES = [ROOT / "index.html", ROOT / "invite" / "index.html"]

# Repositories that are private. A link to one 404s for every visitor.
PRIVATE_REPOS = ("github.com/misttech/airlock", "github.com/misttech/airlock-ui")

# The one origin the page may talk to: the beta form's Google Form. It is
# somewhere the page *sends* to on an explicit click, never somewhere it loads
# from — that distinction is the whole of the no-external-origin rule, so the
# two are checked separately below.
ENDPOINT_PREFIX = "https://docs.google.com/forms/d/e/"
ENDPOINT_SUFFIX = "/formResponse"

# The analytics tag: the one thing the site *loads* from elsewhere, and the one
# thing that observes the reader. Named here so a second tracker cannot arrive
# without someone editing this line and noticing what they are doing.
ANALYTICS_PREFIX = "https://www.googletagmanager.com/gtag/js?id="

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


class Balance(html.parser.HTMLParser):
    """Reports unclosed or mismatched tags."""

    VOID = {"meta", "link", "br", "hr", "img", "input", "source"}

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []

    def handle_startendtag(self, tag, attrs):  # <x /> is balanced by definition
        pass

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            fail(f"mismatched </{tag}> (open: {self.stack[-3:]})")
        else:
            self.stack.pop()


def check_page(page: pathlib.Path) -> str:
    """Structural rules that hold for every page. Returns the page source."""
    name = page.relative_to(ROOT)
    if not page.exists():
        fail(f"{name} is missing")
        return ""
    src = page.read_text()

    parser = Balance()
    parser.feed(src)
    if parser.stack:
        fail(f"{name}: unclosed tags: {parser.stack}")

    # Every asset a page references must exist, or the page ships broken.
    # Resolved against the page's own directory, since invite/ reaches assets
    # with ../ and a root-relative check would call every one of them missing.
    for ref in re.findall(r'(?:href|src|srcset)="([^"]+)"', src):
        if ref.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (page.parent / ref).resolve()
        if not target.exists():
            fail(f"{name}: missing asset: {ref}")

    # Nothing is *loaded* from anywhere else, with one named exception. Every
    # other origin is a third party watching everyone who reads the page.
    for url in re.findall(r'(?:href|src|srcset)="(https?://[^"]+)"', src):
        if url.startswith(ANALYTICS_PREFIX):
            continue
        fail(f"{name}: external origin: {url}")

    # And the site must not tell visitors it has no analytics while loading
    # analytics. The copy said exactly that until the tag was added, directly
    # above the field where someone types their email — a claim like that going
    # stale is worse than never having made it.
    # Comments are stripped first: this is about what a visitor reads, and the
    # tag above is documented in a comment that would otherwise match itself.
    visible = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    if ANALYTICS_PREFIX in src and re.search(r"no analytics|no tracker", visible, re.I):
        fail(f"{name}: loads analytics and also claims not to")

    # A form may *send* to exactly one place, and only the beta endpoint.
    for url in re.findall(r'action="([^"]+)"', src):
        if not (url.startswith(ENDPOINT_PREFIX) and url.endswith(ENDPOINT_SUFFIX)):
            fail(f"{name}: a form posts somewhere that is not the beta endpoint: {url}")

    # The form id and its question ids are filled in by hand, and a page that
    # posts into nowhere looks exactly like one that works.
    for placeholder in sorted(set(re.findall(r"REPLACE_WITH_[A-Z_]+", src))):
        where = "docs/analytics.md" if "GA_" in placeholder else "docs/beta-form.md"
        fail(f"{name}: {placeholder} was never filled in — see {where}")

    # No link into a repository a visitor cannot open.
    for repo in PRIVATE_REPOS:
        if repo in src:
            fail(f"{name}: links to a private repository: {repo}")

    return src


def check_form(name: str, src: str) -> None:
    """The three properties the beta form must keep. See AGENTS.md."""
    # It must post for real, so a visitor with JavaScript disabled gets a
    # submitted form rather than a button that does nothing.
    if 'method="post"' not in src:
        fail(f"{name}: the form no longer posts — it would need JavaScript to work")

    # A cross-origin POST is opaque by design, so a request that never left is
    # invisible unless the page hands over something the visitor can send.
    if 'id="beta-fallback"' not in src or 'id="beta-copy"' not in src:
        fail(f"{name}: the copyable fallback is gone — a failed submit would be silent")

    # And the address stays printed, so there is a way through even if the
    # endpoint is retired.
    if "mailto:getairlock@" not in src:
        fail(f"{name}: the plain mailto link is gone — the endpoint is the only way in")


def main() -> int:
    sources = {p: check_page(p) for p in PAGES}

    # Find the form rather than assume where it lives, so moving it between
    # pages cannot quietly drop its guarantees from this check.
    carrying = [p for p, src in sources.items() if 'id="beta-form"' in src]
    if not carrying:
        fail("no page carries the beta form — the site cannot be signed up to")
    for page in carrying:
        check_form(str(page.relative_to(ROOT)), sources[page])

    # And every page must offer a way to reach it.
    for page, src in sources.items():
        if page in carrying or not src:
            continue
        if 'href="invite/"' not in src and 'href="../invite/"' not in src:
            fail(f"{page.relative_to(ROOT)}: nothing links to the invite page")

    for f in failures:
        print(f"  FAIL  {f}")
    if failures:
        print(f"\n{len(failures)} problem(s)")
        return 1
    print("  all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
