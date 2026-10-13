# Redesign

Improve the look and structure of an existing page. Keep its content: positioning and copy change only through a routed finding.

## 1. Capture the current page

Read the page code, or the live URL the user gives. Write what exists:

- `product-brief.md` from the page and the user input, `Source: user-provided`.
- `content-spec.md` with the current sections and copy word for word, `Source: user-provided`.

Done when: `content-spec.md` lists every section of the current page in its current order.

## 2. Baseline audit → `audit-report.md`

When `audit-report.md` from **audit** mode exists, use it as the baseline and go to step 3.

1. Run `impeccable` critique on the page.
2. Run `web-design-guidelines` on the page code.
3. Run `cro` on `content-spec.md` to find structure problems.

Record each finding with severity and `Route`. A finding that needs new copy or new positioning gets `Route: copywriting` or `Route: product-marketing`; show these to the user and run those stages only for accepted findings.

Done when: every finding has severity and `Route`.

## 3. Concept gate

Propose to the user two or three visual directions that fix the baseline findings, each with typography, colour, and layout idea. Stop and wait for the user to pick one. Write it into `design-spec.md`.

Done when: the user picked one direction.

## 4. Implementation → page code

Run `frontend-design` with the artifacts and the chosen direction. Keep every section of `content-spec.md`.

Done when: the page renders every section of `content-spec.md`, and `design-spec.md` is complete.

## 5. Quality loop

Follow the iteration budget in `SKILL.md`:

1. Run `impeccable` critique, then the commands from the command map for its findings.
2. Run `web-design-guidelines` on the new page code.
3. Fix every `blocker` and `major` finding through its owning stage.
4. Re-check the fixed items.

Done when: `audit-report.md` has no open `blocker` or `major` finding, and every baseline finding is `fixed` or `wontfix` with a reason.
