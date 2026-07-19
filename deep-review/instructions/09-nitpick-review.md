# Nitpick & Minor Comment Review Checklist

## Comment Severity Labeling

- [ ] Every non-mandatory comment has a severity prefix
- [ ] `Nit:` used for minor style/naming suggestions — author can ignore, won't block merge
- [ ] `Optional:` / `Consider:` used for non-critical improvement ideas
- [ ] `FYI:` used for info/observations — no action expected in current PR
- [ ] Blocking issues labeled `BLOCKER`; post-merge tasks labeled `FAST FOLLOW`

## Personal Taste vs. Style Guide

- [ ] No blocking merge based solely on personal style preferences
- [ ] Any style comment NOT covered by official Style Guide → marked `Nit:` or `Optional:`
- [ ] No official rule exists → accept author's variant as-is

## Mentoring Comments

- [ ] Educational comments (new lang features, design patterns) are marked `Nit:`
- [ ] No pressure to refactor working code for educational reasons within current PR

## Perfectionism Avoidance

- [ ] Not requiring author to polish every minor detail before approving
- [ ] PR improving overall readability/maintainability is approved — not blocked over imperfections
- [ ] PR not delayed days/weeks over non-critical nitpicks

## Automation Over Manual Nitpicks

- [ ] Whitespace, alignment, indentation issues NOT raised manually
- [ ] Linters (ESLint, Pylint) and auto-formatters (Prettier, Black) configured in CI
- [ ] Human review focused on logic, architecture, security — not on what tools can enforce
