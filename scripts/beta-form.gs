// Copyright 2026 Mist Tecnologia LTDA. All rights reserved.
// SPDX-License-Identifier: Apache-2.0
//
// Beta signup endpoint for the Airlock site.
//
// This file does not run in this repository. It is the source of a Google Apps
// Script web app, deployed by hand and pasted into index.html as the form's
// action. It lives here so the code that receives other people's email
// addresses is reviewable in a diff like everything else, instead of existing
// only inside one person's Google account.
//
// Deploying it: docs/beta-form.md.

/** Where a new request is announced. A Google Group, so it fans out. */
const NOTIFY = 'getairlock@mist-os.com';

/**
 * Spreadsheet that accumulates the list, or '' to only send mail.
 *
 * Mail alone is a fine start — the group already keeps every request. The
 * sheet earns its place once you want to see the list as a list.
 */
const SHEET_ID = '';
const SHEET_NAME = 'signups';

/** Nothing a person types into this form is longer than this. */
const MAX_FIELD = 500;

/**
 * Handles a submission, whether posted by fetch() or by a plain form
 * navigation from a visitor without JavaScript.
 *
 * Always returns a page rather than JSON: in the no-JavaScript case the
 * browser navigates here and the response *is* what the visitor reads.
 */
function doPost(e) {
  try {
    const params = (e && e.parameter) || {};

    // Honeypot. The field is off-screen and aria-hidden, so a person never
    // sees it and a bot that fills every input does. Report success and drop
    // it: a bot told it failed simply tries something else.
    if (field(params.website)) {
      return page('Thanks', 'Your request is in.');
    }

    const email = field(params.email);
    if (!looksLikeEmail(email)) {
      return page('That address did not look right',
                  'Go back and check it, or mail ' + NOTIFY + ' directly.');
    }

    const about = field(params.about);
    record(email, about);
    announce(email, about);

    return page('Thanks', 'Your request is in. We will mail ' + email + '.');
  } catch (err) {
    // The visitor cannot act on the details, and the details may quote what
    // they typed. Log them; say only that it failed, and how to get through
    // anyway.
    console.error(err);
    return page('That did not go through',
                'Mail ' + NOTIFY + ' directly and we will pick it up.');
  }
}

/** A browser that simply opens the URL should get a sentence, not an error. */
function doGet() {
  return page('Airlock beta signup',
              'This endpoint only accepts the form on the Airlock site.');
}

/** Trims, and refuses to carry an unbounded string any further. */
function field(value) {
  return String(value == null ? '' : value).slice(0, MAX_FIELD).trim();
}

/**
 * Deliberately permissive. The address is confirmed by mailing it, so the
 * only job here is to reject what is obviously not an address — being stricter
 * than the RFC allows is how a form rejects somebody's real email.
 */
function looksLikeEmail(value) {
  return /^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$/.test(value);
}

/** Appends to the sheet, if one is configured. */
function record(email, about) {
  if (!SHEET_ID) return;

  // appendRow is read-then-write underneath, so two submissions landing
  // together can claim the same row. Rare, and cheap to prevent.
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const book = SpreadsheetApp.openById(SHEET_ID);
    const sheet = book.getSheetByName(SHEET_NAME) || book.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['when', 'email', 'what they would run']);
    }
    sheet.appendRow([new Date(), email, about]);
  } finally {
    lock.releaseLock();
  }
}

/** Mails the group, so a request is answerable by replying to it. */
function announce(email, about) {
  MailApp.sendEmail({
    to: NOTIFY,
    replyTo: email,
    subject: 'Airlock beta invite: ' + email,
    body: [
      'A beta invite was requested from the Airlock site.',
      '',
      'Email: ' + email,
      '',
      'What they would run in it:',
      about || '(not said)',
      '',
      'Reply to this message to answer them directly.',
    ].join('\n'),
  });
}

/**
 * The page a visitor without JavaScript lands on. Kept plain on purpose: it is
 * served from googleusercontent.com, so it cannot borrow the site's stylesheet,
 * and a broken half-styled page reads worse than an unstyled one.
 */
function page(title, message) {
  const esc = function (s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  };
  return HtmlService.createHtmlOutput(
    '<!doctype html><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<title>' + esc(title) + '</title>' +
    '<body style="font: 16px ui-monospace, monospace; max-width: 60ch; margin: 3rem auto; padding: 0 1rem">' +
    '<h1 style="font-size: 1.2rem; text-transform: uppercase">' + esc(title) + '</h1>' +
    '<p>' + esc(message) + '</p>' +
    '<p><a href="https://misttech.github.io/airlock-www/">Back to Airlock</a></p>'
  ).setTitle(title);
}
