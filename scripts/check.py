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

    # No external origin: the CSP forbids it, and the page must observe nobody.
    for url in re.findall(r'(?:href|src|srcset)="(https?://[^"]+)"', src):
        fail(f"external origin: {url}")

    # No link into a repository a visitor cannot open.
    for repo in PRIVATE_REPOS:
        if repo in src:
            fail(f"links to a private repository: {repo}")

    # The beta form must keep working without JavaScript.
    if "mailto:getairlock@" not in src:
        fail("the plain mailto link is gone — the form would need JavaScript")

    # ...and must keep working for a visitor whose browser has no mail handler,
    # which is every webmail user. A mailto: alone silently does nothing there.
    if 'id="beta-fallback"' not in src or 'id="beta-copy"' not in src:
        fail("the copyable fallback is gone — the form would need a mail handler")

    for f in failures:
        print(f"  FAIL  {f}")
    if failures:
        print(f"\n{len(failures)} problem(s)")
        return 1
    print("  all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
