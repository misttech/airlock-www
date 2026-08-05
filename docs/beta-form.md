# Deploying the beta form endpoint

The form on the site posts to a Google Apps Script web app. Its source is
[`scripts/beta-form.gs`](../scripts/beta-form.gs); this is how it gets from the
repository into something with a URL.

You need a Google account on the Workspace that owns `mist-os.com` — the script
sends mail as whoever deploys it.

## Why this and not a form service

A form service is a company holding other people's email addresses, and it was
the thing [`AGENTS.md`](../AGENTS.md) argued against when the form was first
built as a `mailto:`. Apps Script is not a new vendor: the mail already lands in
a Google Workspace inbox, so the addresses are somewhere Google can already see.
This adds a handler, not a data processor.

The cost is real and worth naming: the page now has **one external origin**, so
a visitor's browser makes a request to `script.google.com` when they submit.
Only when they submit, and never on load — nothing on this page is *fetched*
from anywhere else. `make check` enforces both halves of that.

## Deploy it

1. Go to [script.google.com](https://script.google.com) and **New project**.
2. Name it `airlock-beta-form`, so it is identifiable in two years.
3. Replace the contents of `Code.gs` with
   [`scripts/beta-form.gs`](../scripts/beta-form.gs).
4. **Deploy → New deployment**, gear icon → **Web app**.
   - *Description*: `airlock-www beta form`
   - *Execute as*: **Me**. It sends mail and writes the sheet as you.
   - *Who has access*: **Anyone**. This is a public web form; "anyone with a
     Google account" would silently reject most visitors.
5. Authorise it when asked. It wants to send mail as you, which is what
   `MailApp.sendEmail` is; the unreviewed-app warning is expected for a script
   you just wrote — **Advanced → Go to airlock-beta-form**.
6. Copy the **Web app URL**. It looks like
   `https://script.google.com/macros/s/AKfycb…/exec`.
7. Paste it into [`index.html`](../index.html) as the form's `action`, replacing
   `REPLACE_WITH_DEPLOYMENT_ID`. `make check` fails until you do.

## Keep the list in a sheet (optional)

Mail alone works — every request is already in the group. A sheet earns its
place once you want to read the list as a list.

Create a spreadsheet, take the id out of its URL
(`docs.google.com/spreadsheets/d/`**`<id>`**`/edit`), and set `SHEET_ID` at the
top of the script. The `signups` tab and its header row are created on the first
submission.

## Redeploying after a change

Apps Script pins each deployment, so editing the code changes nothing that is
live. **Deploy → Manage deployments →** pencil icon **→ Version: New version →
Deploy**. The URL survives, so `index.html` does not change.

Deploying as a *new deployment* instead mints a new URL and leaves the old one
serving the old code — which is occasionally what you want, and never what you
want by accident.

## Check it

With the URL in place:

```sh
make check     # fails while the placeholder is still there
make serve
```

Submit the form. Within a few seconds a mail should arrive at
`getairlock@mist-os.com`, with the requester's address as the reply-to, so
answering it replies to *them* and not to the group.

Then submit again with JavaScript disabled. The browser should navigate to a
plain confirmation page served by the endpoint. That path is the one that keeps
working when everything else fails, so it is worth actually exercising rather
than assuming.

## What arrives

| field | where it comes from |
|---|---|
| `email` | the address they typed, required |
| `about` | what they would run in it, optional |
| `website` | the honeypot — off-screen, `aria-hidden`, always empty for a person |

A submission with `website` set is answered with a success page and dropped. A
bot told it failed just tries something else.

There is no CAPTCHA. If the honeypot stops being enough, the next step is a
timestamp check — a form completed in under two seconds was not completed by a
person — before anything that makes a visitor prove themselves.
