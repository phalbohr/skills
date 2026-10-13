# Create

Build a new landing page. Each step names its skip condition; a skipped step still writes its `Source:` line.

## 1. Product input

Collect the product description: from the user, the repository README, or the product website the user names. If the user can give no description, ask for one and stop.

Done when: you can state what the product does, for whom, and the page's single conversion goal.

## 2. Positioning → `product-brief.md`

Run `product-marketing` when the target audience or the positioning is unclear. When the user already supplied both, fill the template from the user input and write `Source: user-provided`.

Done when: every field of `product-brief.md` has content or `unknown` with a reason.

## 3. Copy → `content-spec.md`

Run `copywriting` when the user has no finished copy. When the user supplied copy, put it into the template unchanged and write `Source: user-provided`.

Done when: every section in `Sections` has a headline, body, and its CTA or `no CTA`.

## 4. Structure review → `CRO notes`

Run `cro` on `content-spec.md`. Skip only when the user fixed the section order, for example by a brand template.

Show the notes to the user. `copywriting` applies the accepted notes; mark each note `accepted` or `rejected`.

Done when: every CRO note has a status.

## 5. Concept gate

Propose to the user:

- the section order from `content-spec.md`;
- two or three visual directions, each with typography, colour, layout idea, and one reference mood.

Stop and wait for the user to pick a direction. Write the chosen direction into `design-spec.md`.

Done when: the user picked one direction.

## 6. Implementation → page code

Run `frontend-design` with `product-brief.md`, `content-spec.md`, and the chosen direction. When the user supplied a finished design, implement that design and write `Source: user-provided` for the visual direction.

Done when: the page renders every section of `content-spec.md` in the stated order, and `design-spec.md` is complete.

## 7. Quality loop → `audit-report.md`

Follow the iteration budget in `SKILL.md`:

1. Run `impeccable` critique, then the commands from the command map for its findings.
2. Run `web-design-guidelines` on the page code.
3. Record each finding in `audit-report.md` with severity and `Route`.
4. Fix every `blocker` and `major` finding through its owning stage.
5. Re-check the fixed items.

Skip `landing-page-conversion-audit`: a new page has no traffic data.

Done when: `audit-report.md` has no open `blocker` or `major` finding.
