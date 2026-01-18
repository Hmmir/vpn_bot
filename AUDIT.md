# GetniusVPN Audit (Strict)

Below is a deliberately harsh audit of UX/UI, product flows, and engineering quality. No compliments — only issues and what to improve.

## UX/UI issues

- [CRITICAL] Onboarding does not explain *what the user should do next* in a single, scannable step. The first screen is a wall of text and asks to choose a device without telling *why* or *what happens next*. Use a one‑line instruction + CTA and keep details in collapsible help.
- [CRITICAL] The “Profile” screen does not show a clear subscription state, plan name, or expiry if the key is missing. The user sees nothing actionable. Replace with a decisive CTA (“Оплатить тариф”) and explain the flow.
- [HIGH] Button hierarchy is confusing: duplicate messages and multiple message bubbles repeat the same content, which feels spammy. Consolidate each section into one bubble with a clear CTA.
- [HIGH] Install flow lacks a quick “Test connection” or “Copy key” confirmation. Users copy keys manually but there is no UI feedback or helper.
- [HIGH] The trial pricing is hidden inside a paragraph; there is no “Trial” CTA with clear price/term. The competitor highlights trial as a separate card.
- [HIGH] No visual differentiation between free/trial/pro states. Users can’t tell why they should pay.
- [HIGH] Two‑column inline buttons appear in device selection but the rest of the UI is single‑column; style inconsistency reduces trust.
- [MEDIUM] The menu is in the keyboard, but the bot sends “menu hint” in another message which can confuse users. Remove redundant hints and focus on primary CTAs.
- [MEDIUM] “Other devices” path is a generic text with no per‑platform shortcuts (Windows/MacOS/iOS). Add platform‑specific buttons or links.
- [MEDIUM] Russian/English UX is inconsistent: the RU version is verbose, EN is short. Keep a symmetric tone so product feels consistent.
- [LOW] Visual cards are neon + dark but the rest of the bot uses plain text; the style feels disconnected. Either use card‑first UX or minimal text‑only UX.

## Product flow gaps

- [CRITICAL] No automated payment confirmation path is wired end‑to‑end. User pays → key is not guaranteed unless webhook is configured and running.
- [CRITICAL] No “payment pending / failed” state. Users who paid but didn’t receive key have no recovery flow.
- [HIGH] No automatic key rotation or re‑issue if a user loses the key.
- [HIGH] No device limit or traffic limit messaging; user expectation is unclear.
- [HIGH] No in‑bot SLA for support, no escalation, no ticket IDs → support is messy under load.
- [MEDIUM] Referral flow lacks attribution confirmation and reward status (“you earned +1 month”).

## Engineering & architecture

- [CRITICAL] SQLite used for subscriptions/reminders with no concurrency handling or retry/backoff; simultaneous writes can lock DB under load.
- [HIGH] XUI API calls have no timeouts/retries/backoff; any API hiccup will break issuing.
- [HIGH] Error paths are silent: failed media sends, failed API calls, and DB errors are not reported to admins.
- [HIGH] Hardcoded text content in code; no CMS/translation layer. Any copy update is a deployment.
- [MEDIUM] The bot uses in‑memory language map and DB language; no sync on restart (lost user language state for active session).
- [MEDIUM] Webhook auth is a static token in query/header only; no signature verification. This is weak for payments.
- [MEDIUM] No structured logging; hard to debug real incidents.
- [LOW] Missing tests: no unit tests for XUI integration or webhook, no smoke tests.

## Ops / reliability

- [CRITICAL] Only one server = single point of failure. No automatic failover or traffic shift.
- [HIGH] No external monitoring/alerting for latency, packet loss, or geo‑specific blocks.
- [HIGH] No runbook for rotating domains/ports under block. Recovery is manual.
- [MEDIUM] No TLS cert monitoring for x‑ui panel/subscription endpoints.
- [MEDIUM] No automatic geo file updates or Xray updates schedule (risk of blocks).

## Security

- [HIGH] Admin commands are only guarded by user ID; no signed admin sessions or rate limiting.
- [HIGH] Token exposure risk if `.env` leaks; no vault/secret management.
- [MEDIUM] No IP allowlist for admin panel or webhook server.

## Visual design issues (harsh)

- [HIGH] Card visuals are highly saturated neon gradients; combined with Telegram dark UI they can feel “cheap” and scam‑like for some users.
- [HIGH] Typography hierarchy is weak; there is no consistent type scale between cards and chat messages.
- [MEDIUM] CTA labels are too generic (“Подключить”), no value promise (e.g., “Подключить за 1 минуту”).
- [LOW] Icons in cards are generic and inconsistent with brand identity.

## Immediate next improvements (priority order)

1. Implement payment‑to‑key flow reliably (webhook + retries + admin alert on failure).
2. Add subscription state in profile (plan, expiry date, renewal CTA).
3. Add multi‑inbound/entry points and a “switch server” button in bot.
4. Add monitoring + alerting + update checks (x‑ui/xray).
5. Tighten UX: remove duplicate messages, reduce text length, add explicit “Copy key” action.
