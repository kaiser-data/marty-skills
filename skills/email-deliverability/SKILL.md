---
name: email-deliverability
description: "Diagnose and prevent email deliverability problems: spam-folder placement, silent filtering, bounces, sender reputation, and pre-/post-send campaign checks in any ESP (Brevo, CleverReach, Mailchimp, SendGrid, Mailjet, …). Use when a sent email lands in spam or a recipient reports not receiving it, when analyzing campaign delivery metrics or bounces, before a mass send, or for unsubscribe/GDPR list hygiene."
---

# Email Deliverability

Get campaign mail into inboxes and diagnose it correctly when it doesn't arrive. Distilled from real campaign operations (162-recipient sends via Brevo, AOL spam incident investigated to root cause); the workflow is ESP-neutral — every serious sender (Brevo, CleverReach, Mailchimp, SendGrid, Mailjet) exposes the same primitives: per-recipient message events/log, bounce list, test send, unsubscribe placeholder. Find those four in whatever ESP the user has, then work the checklists. For writing the HTML itself, use the companion `html-email` skill.

## Diagnosing "I didn't get the email"

Work in this order — most reports are NOT delivery failures:

1. **Check the sending system's per-recipient log first** (Brevo "message events", CleverReach report/recipient detail, Mailchimp activity feed — every ESP has one). "Delivered" + recipient can't find it almost always means **spam folder**, not a failed send.
2. AOL and Yahoo in particular filter legitimate mail to spam **without a hard bounce** — the sender-side status stays "delivered".
3. Match any hard bounce in campaign metrics to its actual recipient before drawing conclusions — a bounce in the same campaign may belong to a completely different address than the person complaining.
4. Only after ruling out spam-folder and bounce: check for typos in the stored address, full mailbox, or provider-level blocks.

## Remediation that actually improves reputation

- Have the recipient **mark the mail "not spam"** and **add the sender address to their contacts**. This improves the sender's reputation at that provider for **all** future recipients there, not just this one.
- For hard-bounced addresses: remove or correct them before the next send — repeated bounces damage sender reputation.
- Honor unsubscribes immediately and purge them from every list (GDPR); zero-unsubscribe streaks after a cleanup are a health signal worth tracking.

## Pre-send checklist

- Working `{{ UNSUBSCRIBE }}` link and a "why you're receiving this" consent line in the footer — legally required and a strong spam-score factor.
- HTML under ~90 KB: Gmail clips at ~102 KB and the clipped view hides the footer — unsubscribe link AND tracking pixel gone (spam complaints rise, opens under-report).
- Real test sends to at least Outlook, Gmail, and one mobile client; review in the actual inbox, not a screenshot. Expect 2–3 iterations.
- **Preflight with mail-tester.com** (free, ~3 tests/day): send the campaign to its generated address and fix anything below ~9/10 — it scores SPF/DKIM/DMARC, spam triggers, HTML weight, and broken links in one shot. More render/spam tools for the user: the "Testing tools" section of the html-email skill's client-quirks reference.
- Send from a domain-aligned address (SPF/DKIM/DMARC configured for the sending platform — most ESPs have a domain-authentication wizard; mail-tester verifies the result).
- Few distinct link domains; one repeated primary CTA URL is fine.
- Segment per language/list so recipients get the variant they signed up for — irrelevant content drives spam complaints.

## Post-send monitoring

- Watch delivered/bounced counts the same day; investigate every hard bounce individually.
- Track opens and unsubscribes over the following days — rising opens with zero unsubscribes indicates healthy list + content.
- Log incidents and their resolution (who, provider, cause, fix) so the next campaign starts from evidence.
