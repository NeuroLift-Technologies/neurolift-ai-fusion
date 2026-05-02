# Review Reports (`docs/reviews/`)

This directory stores source-verified engineering review reports that summarize
open items for humans or the next agent. Use it for review artifacts that are
broader than a single session handoff, such as PR review analysis, open-items
queues, and cross-thread status reports.

## When to add a review report

Add a report here when the work product is primarily analysis, not a runtime or
feature document. Good fits include:

- open PR, issue, blocker, or unresolved-review-comment inventories
- review summaries for a specific PR or branch
- source-verified risk reports that future contributors should consult

Do not use this folder for standard session handoffs. Session-end handoff JSON
belongs in `docs/agent-log/handoffs/`.

## Source requirements

Review reports must distinguish verified facts from recommendations. Before
recording a claim, cite or name the source used to verify it:

- repository files, for example `docs/active-threads.md`
- handoff records, for example `docs/agent-log/handoffs/*.json`
- GitHub PR, issue, or review metadata inspected with `gh`
- source files and test files when a report discusses code behavior

If a finding applies only to a non-default branch or historical PR, state that
scope explicitly so readers do not assume it affects the current branch.

## Recommended structure

Use short, scan-friendly sections:

```markdown
# <Report Title>

**Reviewer:** <agent or human>
**Session ID:** <id if available>
**Date:** <YYYY-MM-DD>
**Branch reviewed:** `<branch or commit>`
**Thread:** TH-XXX

## Purpose
Why this report exists and who should use it.

## Blockers
Facts that prevent progress, with source references.

## Decisions Pending
Human or maintainer decisions still required.

## Open Pull Requests / Issues / Comments
Inventories with current state and recommended next action.

## Prioritized Work Queue
Ordered next steps, keeping recommendations separate from verified state.
```

## Current examples

- `2026-05-02-copilot-open-items-review.md` documents TH-007 open items after
  PR #46 and covers open PRs, unresolved review comments, blockers, and pending
  decisions as of 2026-05-02.
- `pr_23_review.md` is a PR-specific review report that analyzes code-level
  correctness and maintainability findings.

## Common pitfalls

- **Stale inventories:** Include the review date and branch/commit so future
  readers know when to re-check GitHub state.
- **Branch confusion:** State when a problem belongs to a PR branch rather than
  the current working branch.
- **Unverified behavior:** Do not infer runtime behavior from a report alone;
  inspect the referenced source files when documenting code contracts.
- **Handoff overlap:** Keep resumability details in handoff JSON and broader
  cross-thread analysis in review reports.
