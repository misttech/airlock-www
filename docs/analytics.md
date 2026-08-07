# Analytics

The site loads **Google Analytics 4** on both pages. This is the only thing it
loads from anywhere but this repository.

## Wiring it up

1. [analytics.google.com](https://analytics.google.com) → create a property for
   `airlock.mist-os.com` if there is not one → **Data streams** → **Web**.
2. Copy the **Measurement ID**. It looks like `G-XXXXXXXXXX`.
3. Paste it over `REPLACE_WITH_GA_MEASUREMENT_ID` in both
   [`index.html`](../index.html) and [`invite/index.html`](../invite/index.html)
   — it appears **twice per page**, once in the script `src` and once in the
   `gtag("config", …)` call. `make check` fails until every one is replaced.

There is no build step, so the id is in the markup rather than injected. It is
not a secret — it ships to every visitor either way — but it is worth knowing it
is public, because it is the kind of string people assume is not.

## What this cost

Two things that were true before and are not now, both recorded rather than
quietly dropped:

**The site loads a third-party script on every page view.** Not on an action —
on arrival, for everybody, before anyone decides to do anything. That is a
different thing from the form endpoint, which a visitor triggers by clicking a
button, and `AGENTS.md` keeps them as separate rules for that reason.

**The invite page said it had no analytics.** It said so directly above the
field where somebody types their email address, on a site whose argument is that
untrusted things should be watched and people should not be. That sentence was
rewritten in the same commit that added the tag, and `scripts/check.py` now fails
the build if any page loads analytics while claiming not to. The tag is a choice;
the claim going stale would have been a lie, and only one of those is worth a
machine check.

## Consent — decide this

**This is not wired up, and it is the open question here.**

GA4 sets cookies and sends visitor IP addresses to Google. In the EU and UK,
ePrivacy plus GDPR means that needs prior consent — a banner, with analytics off
until someone accepts. Under Brazil's LGPD the analysis is less settled but the
cautious reading lands in the same place, and Mist Tecnologia is a Brazilian
company with an international audience.

Three ways out, in the order they cost:

1. **A cookieless analytics tool instead** — Cloudflare Web Analytics (free),
   GoatCounter, Plausible, Fathom. No cookies, no personal data, no banner in
   most readings, and page views are the only thing this site actually needs to
   know. This removes the problem rather than managing it, and it is what I
   would reach for if the question is only "does anyone visit".
2. **GA with Consent Mode v2** — the tag loads but stores nothing until consent,
   and a banner grants it. Keeps GA, adds a banner and about a day of care.
3. **Ship as is and accept the exposure.** Defensible for a pre-launch page with
   little traffic. Worth revisiting before anything is promoted.

Whatever is chosen, write down which and why, here, in this file.

## Removing it

Delete the two `<script>` blocks from the `<head>` of both pages, drop
`ANALYTICS_PREFIX` and the two checks that use it from `scripts/check.py`, and
restore the "no analytics" wording on the invite page. Everything else is
unaffected — nothing on the site depends on the tag being present.
