# airlock-www

The website for Airlock, published to GitHub Pages.

## No build step

The site is HTML and CSS, served exactly as written. There is no static site
generator, no bundler, and no dependency to update — which means the page is
reviewable in a diff and cannot break because a toolchain moved underneath it.

To work on it, open `index.html` in a browser, or serve the directory:

```sh
python3 -m http.server 8000
```

## Design

The stylesheet is the same system the Airlock dashboard uses, adapted from
[The Monospace Web](https://github.com/owickstrom/the-monospace-web) (MIT) and
reduced to what a document needs. Everything lands on a character grid. For a
tool whose primary interface is a terminal, that is the honest aesthetic.

JetBrains Mono is self-hosted (OFL-1.1, 32 KB latin subset) rather than pulled
from a CDN — the same choice the dashboard makes, for the same reason.

Exactly one colour exists, and it is used for one thing: the status notice. The
project is early, and a landing page that buried that would be selling
something its own documentation contradicts.

## Separate repo, on purpose

This lives outside the `airlock` repository so that a web toolchain never lands
there, and so the site can be public while the code is not.

Claims on this page are drawn from the Airlock README and its documentation.
**If a claim here outruns what those say, the page is wrong** — particularly
around tenant isolation, which the project documents honestly and this page must
not oversell.

This repository is public while the Airlock repositories are not, so the page
links to no internal document. Add those links only when the code repository is
public and the links will actually resolve for a visitor.
