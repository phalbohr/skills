# Audit

Find problems on an existing page and recommend fixes. Change no page code and no copy; the only output is `audit-report.md`.

## 1. Inputs

Get from the user:

- the page URL or code;
- the traffic sources, especially paid ads and their ad copy;
- analytics: visits, conversions, conversion rate, device split, the funnel after the CTA.

Missing data does not block the audit. Write each missing item into `Data limits` in `audit-report.md`.

Done when: every input above is present or listed in `Data limits`.

## 2. Conversion audit

Run `landing-page-conversion-audit`. Skip it only when the page has no traffic yet; then write the reason into `Data limits` and rely on `cro` for structure.

Done when: message match, above the fold, offer clarity, friction, trust, funnel, and measurement each have a finding or `no issue`.

## 3. Structure, UX, and visual audit

1. Run `cro` for page structure and copy.
2. Run `web-design-guidelines` for UX and accessibility.
3. Run `impeccable` critique for visual design.

Done when: each of the three skills has produced its findings.

## 4. Report → `audit-report.md`

Merge and de-duplicate the findings. Rank them by expected impact on conversion. Give the top seven a full entry; list the rest under `Other findings`.

Each finding states its fix type: `fix now` for a clear defect, `test` for a hypothesis that needs an A/B test.

Done when: every finding has severity, evidence, fix, effort, confidence, fix type, and `Route`.

To apply the fixes, the user starts **redesign** mode with this report as the baseline audit.
