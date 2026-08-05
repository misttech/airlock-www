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
PAGE = ROOT / "index.html"

# Repositories that are private. A link to one 404s for every visitor.
PRIVATE_REPOS = ("github.com/misttech/airlock", "github.com/misttech/airlock-ui")

# The one origin the page may talk to: the beta form's endpoint, whose source is
# scripts/beta-form.gs. It is somewhere the page *sends* to on an explicit
# click, never somewhere it loads from — that distinction is the whole of the
# no-external-origin rule, so the two are checked separately below.
ENDPOINT_PREFIX = "https://script.google.com/macros/s/"
ENDPOINT_PLACEHOLDER = "REPLACE_WITH_DEPLOYMENT_ID"

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


def main() -> int:
    src = PAGE.read_text()

    parser = Balance()
    parser.feed(src)
    if parser.stack:
        fail(f"unclosed tags: {parser.stack}")

    # Every asset the page references must exist, or the page ships broken.
    for ref in re.findall(r'(?:href|src|srcset)="([^"]+)"', src):
        if ref.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if not (ROOT / ref).exists():
            fail(f"missing asset: {ref}")

    # Nothing is *loaded* from anywhere else. This is the rule that keeps the
    # page from observing its visitors, and it has no exceptions.
    for url in re.findall(r'(?:href|src|srcset)="(https?://[^"]+)"', src):
        fail(f"external origin: {url}")

    # A form may *send* to exactly one place, and only the beta endpoint.
    for url in re.findall(r'action="([^"]+)"', src):
        if not url.startswith(ENDPOINT_PREFIX):
            fail(f"a form posts somewhere that is not the beta endpoint: {url}")
        elif ENDPOINT_PLACEHOLDER in url:
            fail(
                "the beta endpoint is still the placeholder — deploy "
                "scripts/beta-form.gs and paste its URL (docs/beta-form.md)"
            )

    # No link into a repository a visitor cannot open.
    for repo in PRIVATE_REPOS:
        if repo in src:
            fail(f"links to a private repository: {repo}")

    # The beta form must post for real, so a visitor with JavaScript disabled
    # gets a submitted form rather than a button that does nothing.
    if 'method="post"' not in src:
        fail("the form no longer posts — it would need JavaScript to work")

    # A cross-origin POST is opaque by design, so a request that never left is
    # invisible unless the page hands over something the visitor can send.
    if 'id="beta-fallback"' not in src or 'id="beta-copy"' not in src:
        fail("the copyable fallback is gone — a failed submit would be silent")

    # And the address stays printed, so there is a way through even if the
    # endpoint is retired.
    if "mailto:getairlock@" not in src:
        fail("the plain mailto link is gone — the endpoint is the only way in")

    for f in failures:
        print(f"  FAIL  {f}")
    if failures:
        print(f"\n{len(failures)} problem(s)")
        return 1
    print("  all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
