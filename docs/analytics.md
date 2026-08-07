# Analytics

The site loads **Google Analytics 4** on both pages. This is the only thing it
loads from anywhere but this repository.

**The tag is already in the markup.** `index.html` and `invite/index.html` each
carry the GA snippet in their `<head>`. The only thing missing is the
measurement id, which is an account-specific string only you can produce. That
is what the rest of this page is about.

---

## 1. Create the property

Do this from the Google account that should **own** the data — a
`@mist-os.com` / Workspace account, not a personal one. Ownership is painful to
move later, and analytics tied to somebody's personal Gmail is a small hostage
situation.

Google renames things in this flow every few months. The labels below are what
they are called now; the shape has been stable even when the wording moves.

1. Go to [analytics.google.com](https://analytics.google.com).
2. If you have no account yet: **Start measuring**. If you do: **Admin** (bottom
   left) → **Create** → **Property**.
3. **Account** — one per company, not per site.
   - *Account name*: `Mist Tecnologia`
   - *Data sharing settings*: four checkboxes, all optional, all on by default.
     They share your data with Google for benchmarking, technical support and
     product improvement. **Uncheck them.** None of them measure your site;
     they only widen who sees it.
4. **Property** — one per site.
   - *Property name*: `Airlock`
   - *Reporting time zone*: the one you will read the numbers in.
   - *Currency*: irrelevant here — nothing is being bought.
5. **Business details** — industry and company size. Used for benchmarking
   comparisons you unchecked in step 3. Answer or don't.
6. **Business objectives** — pick *Examine user behavior*. It only preselects
   which reports appear; nothing about collection changes.
7. **Terms of Service** — choose **Brazil**, accept. Also accept the **Data
   Processing Terms** when offered; that is the GDPR processor agreement and you
   want it on record before any EU visitor arrives, not after.

## 2. Create the web data stream

The property is the container; the stream is the actual site.

1. **Data collection and modification** → **Data streams** → **Add stream** →
   **Web**.
2. *Website URL*: `https://airlock.mist-os.com`
3. *Stream name*: `airlock.mist-os.com`
4. **Enhanced measurement** — on by default. It adds automatic events beyond
   page views: scroll depth, outbound clicks, site search, file downloads, video
   engagement, and **form interactions**.

   That last one matters here. This site has exactly one form, and it collects
   email addresses. Enhanced measurement does not capture what people type — it
   records that a form was started and submitted — but it is worth deciding
   deliberately rather than leaving on because it was on. Scroll depth and
   outbound clicks are the only ones with an obvious use on a two-page site.

5. **Create stream**.

## 3. Get the measurement id

The stream detail panel shows it top right:

```
Measurement ID    G-XXXXXXXXXX
```

That string is what goes in the pages. **It is not a secret** — it ships to
every visitor in the page source either way. Worth saying because it looks like
the kind of string that should be one, and people occasionally hide it in a
secret store and then wonder why a static site cannot read it.

## 4. Do NOT paste Google's snippet

Google will offer you **View tag instructions** → *Install manually*, showing a
block of `<script>` to paste into your `<head>`.

**Ignore it.** That snippet is already in both pages, committed and reviewed.
Pasting Google's copy alongside it loads `gtag.js` twice and double-counts every
page view — a failure that looks like unexpectedly good traffic rather than like
a bug, which is the worst way for a metric to be wrong.

You need one string from that screen, not the block around it.

## 5. Put the id in the pages

Replace `REPLACE_WITH_GA_MEASUREMENT_ID` with your `G-XXXXXXXXXX`:

| file | occurrences |
|---|---|
| [`index.html`](../index.html) | 2 — the script `src`, and the `gtag("config", …)` call |
| [`invite/index.html`](../invite/index.html) | 2 — same two |

Four in total. Then:

```sh
make check     # fails while any placeholder remains
```

## 6. Settings worth changing before you forget

In **Admin**, once the property exists:

- **Data retention** — *Data settings → Data retention*. Defaults to 2 months
  for event data; 14 is the maximum. Longer is not better: it is more personal
  data held for longer, for a site whose whole question is "did anyone visit".
  Leave it at 2 unless you have a reason.
- **Google signals** — *Data settings → Data collection*. Off by default.
  **Leave it off.** It turns on cross-device tracking tied to signed-in Google
  accounts, which is a materially bigger privacy claim and drags consent
  requirements with it. It buys demographics reports this site has no use for.
- **Internal traffic** — *Data streams → your stream → Configure tag settings →
  Define internal traffic*. Add your own IP so your own visits do not become the
  numbers. On a low-traffic pre-launch page you are otherwise most of the graph.

## 7. Verify it

After merging and deploying, with the real id in place:

1. **Realtime** in GA — open `https://airlock.mist-os.com` in another tab and
   watch the active-user count. It appears within seconds. If it does not, GA is
   not receiving anything and the rest of this is moot.
2. **In the browser console**, on the live site:

   ```js
   typeof gtag                                    // "function"
   dataLayer.map(a => a[0])                       // includes "js" and "config"
   document.querySelector('script[src*=gtag]').src // your G- id, once
   ```

   That last one is the double-tag check from step 4 — if two scripts match,
   somebody pasted the snippet.
3. **An ad blocker will block all of this.** Test in a clean profile before
   concluding it is broken. This also means your numbers are an undercount, by a
   margin that is larger than usual for an audience of developers.

---

## What this cost

Two things that were true before and are not now, recorded rather than quietly
dropped:

**The site loads a third-party script on every page view.** Not on an action —
on arrival, for everybody, before anyone decides to do anything. That is a
different thing from the form endpoint, which a visitor triggers by clicking a
button, and [`AGENTS.md`](../AGENTS.md) keeps them as separate rules for that
reason.

**The invite page said it had no analytics.** It said so directly above the
field where somebody types their email address, on a site whose argument is that
untrusted things should be watched and people should not be. That sentence was
rewritten in the same commit that added the tag, and
[`scripts/check.py`](../scripts/check.py) now fails the build if any page loads
analytics while claiming not to. The tag is a choice; the claim going stale
would have been a lie, and only one of those is worth a machine check.

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
`ANALYTICS_PREFIX` and the two checks that use it from
[`scripts/check.py`](../scripts/check.py), and restore the "no analytics"
wording on the invite page. Everything else is unaffected — nothing on the site
depends on the tag being present.
