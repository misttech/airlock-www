# Wiring up the beta form

The form on the site posts to a Google Form. There is nothing to deploy and no
code to run — you create the Form, copy three ids into
[`index.html`](../index.html), and it works.

## Why a Form and not a script

The obvious answer was a Google Apps Script web app: our own code, our own
repository, a real handler. Its consent screen asks for two things, and reading
them out loud settles it:

> **See, edit, create, and delete all your Google Sheets spreadsheets**
> **Send email as you**

That is a lot of authority to hold permanently so that a signup box works, and
the first one is not even needed — Apps Script decides scopes by scanning the
source, so a spreadsheet call that never runs still asks for every spreadsheet
you own.

A Form grants nothing. Posting to its `formResponse` URL is exactly what the
Form's own page does; there is no OAuth screen, no deployment, and no code
executing as anyone. Google stores the responses and mails you about them.

**The cost, stated plainly:** `formResponse` is not a documented API. It has
worked this way for over a decade and every "custom front-end for Google Forms"
guide relies on it, but Google has never promised it. If they change it,
submissions fail and — because a cross-origin POST is opaque — the page cannot
tell. Which is why the [checking](#check-it) step below is not optional, and why
the printed address stays on the page.

## Create the Form

1. [forms.new](https://forms.new). Title it `Airlock beta invite`.
2. First question: **Your email**, short answer.
   - ⋮ → **Response validation** → *Text* → *Email address*.
   - Mark it **Required**.
   - Do **not** use Settings → *Collect email addresses*. That path names its
     field `emailAddress` instead of an `entry.N`, and in a Workspace it can
     demand the visitor be signed in.
3. Second question: **What you would run in it**, paragraph, **not** required.
4. **Publish** → **Published options**. This is the step that quietly breaks
   everything if missed:
   - **Responders: Anyone with the link.** Inside a Workspace this defaults to
     the organisation only, which turns every outside submission into a sign-in
     wall — and it fails in the one way you will not notice, because you can
     always reach your own form.
   - *Accepting responses* — on.
   - **Save.**

   Older Forms accounts show this as **Settings → Restrict to users in
   mist-os.com → off** instead. Same setting, same consequence.
5. **Settings** (gear), for two more:
   - *Limit to 1 response* — **off**. It requires a Google account.
   - *Response receipts* — optional, and pleasant: Google mails the requester a
     copy of what they sent, so they get a confirmation and we still grant
     nothing.

Do not take the form id from **Copy responder link** — it may hand you a
shortened `forms.gle/…`, which does not contain one. The pre-filled link below
always gives the long form.

## Get the three ids

⋮ (top right) → **Get pre-filled link**. Type anything into both questions →
**Get link** → **Copy link**. You get:

```
https://docs.google.com/forms/d/e/1FAIpQLSc…/viewform?usp=pp_url
    &entry.1234567890=whatever
    &entry.9876543210=whatever
```

Three values, in the order they appear:

| placeholder in `index.html` | from the pre-filled link |
|---|---|
| `REPLACE_WITH_FORM_ID` | the `1FAIpQLSc…` between `/d/e/` and `/viewform` |
| `REPLACE_WITH_EMAIL_FIELD_ID` | the first `entry.N` — the email question |
| `REPLACE_WITH_ABOUT_FIELD_ID` | the second `entry.N` |

Note the form's action ends in **`/formResponse`**, not `/viewform`. `make
check` enforces that, along with there being no `REPLACE_WITH_` left anywhere.

## Get told about a response

Form editor → **Responses** → ⋮ → **Get email notifications for new responses**.
That mails whoever switched it on, so turn it on from an account that reads
`getairlock@mist-os.com`.

The group is still worth keeping: the page prints the address, and some people
will always rather write a sentence than fill in a box. Those go to the group as
they always did, and the auto-reply still answers them.

Optionally **Link to Sheets** for the list as a spreadsheet. It is a plain
spreadsheet Google fills in — still no grant, since nothing of ours is reading
it.

## Check it {#check-it}

```sh
make check     # fails while any REPLACE_WITH_ remains
make serve
```

Then submit, **from a browser signed out of Google or in a private window** —
signed in as the form's owner is the one case that proves nothing, because
that account can reach the form whether or not outsiders can.

- The page should show *Your request is in*.
- The response should appear under **Responses** within a few seconds.
- If it does not, the Workspace restriction in step 4 is the first thing to
  check.

Then submit once with JavaScript disabled. The browser navigates to Google's
*Your response has been recorded* page. That path is the one that still works
when everything else fails, so exercise it rather than assume it.

## Spam

The page carries a honeypot: an off-screen, `aria-hidden` field a person never
meets. If it comes back filled, the script reports success and sends nothing.

It catches bots that drive the page. A bot posting straight to Google's endpoint
is not something a static site can stop, and a Form has no spam filtering of its
own — so if junk starts arriving, the answer is a filter on the responses sheet,
or moving to an endpoint that can think. Not a CAPTCHA, which taxes every real
visitor to inconvenience someone who has already bypassed the page.
