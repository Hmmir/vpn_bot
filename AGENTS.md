## Continuity Ledger (compaction-safe)

Maintain a single Continuity Ledger for this workspace in `CONTINUITY.md`. The ledger is the canonical session briefing designed to survive context compaction; do not rely on earlier chat text unless it's reflected in the ledger.

### How it works

- At the start of every assistant turn: read `CONTINUITY.md`, update it to reflect the latest goal/constraints/decisions/state, then proceed with the work.
- Update `CONTINUITY.md` again whenever any of these change: goal, constraints/assumptions, key decisions, progress state (Done/Now/Next), or important tool outcomes.
- Keep it short and stable: facts only, no transcripts. Prefer bullets. Mark uncertainty as `UNCONFIRMED` (never guess).
- If you notice missing recall or a compaction/summary event: refresh/rebuild the ledger from visible context, mark gaps `UNCONFIRMED`, ask up to 1-3 targeted questions, then continue.

### `functions.update_plan` vs the Ledger

- `functions.update_plan` is for short-term execution scaffolding while you work (a small 3-7 step plan with pending/in_progress/completed).
- `CONTINUITY.md` is for long-running continuity across compaction (the "what/why/current state"), not a step-by-step task list.
- Keep them consistent: when the plan or state changes, update the ledger at the intent/progress level (not every micro-step).

### In replies

- Begin with a brief "Ledger Snapshot" (Goal + Now/Next + Open Questions). Print the full ledger only when it materially changes or when the user asks.

### `CONTINUITY.md` format (keep headings)

- Goal (incl. success criteria):
- Constraints/Assumptions:
- Key decisions:
- State:
    - Done:
    - Now:
    - Next:
- Open questions (UNCONFIRMED if needed):
- Working set (files/ids/commands):

# AGENTS.md

Guidelines for contributors and AI agents working on the GetniusVPN bot repository.

## 1) Core rules
- Do not edit production directly. All changes go through git.
- If `CHANGELOG.md` exists, update it for meaningful changes.
- Prefer small, reversible changes with clear rollback steps.
- Keep secrets out of git. Use `.env` and server secrets only.

## 2) Repository layout (high level)
- `src/`: Bot logic, handlers, and localization.
- `assets/`: Static images/icons used by the bot.
- `content/`: Message templates, onboarding copy, and FAQ text.
- Root docs: setup guides, runbooks, and release notes.

## 3) Local development
- Install dependencies per `package.json` or `pyproject.toml` (UNCONFIRMED).
- Configure `.env` from an example file if present.
- Run the bot with the standard dev script in the repo (UNCONFIRMED).

## 4) Tests and quality
- Run linters/tests if configured in the repo.
- Add tests for new flows when feasible (especially onboarding, payments, and support).

## 5) Safe release workflow
- Build and test locally or on staging before production.
- Back up any stateful services (DB/Redis) before migrations.
- Apply migrations, then restart services.
- Run smoke tests.

## 6) Smoke tests (minimum)
- `/start` onboarding works and shows device selection.
- Device install flow returns correct instructions and buttons.
- тарифы/оплата flow opens correct links and handles callback.
- Профиль shows key, status, and referral link correctly.
- Support/FAQ flow routes to correct sections.

## 7) Rollback
- Revert to a previous commit/tag.
- Rebuild and redeploy.
- If migrations changed data, restore from backup.

## 8) When updating features
- Update docs if the change affects operations or support.
- If security-related, update `SECURITY.md` if present.
