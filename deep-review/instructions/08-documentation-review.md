# Documentation Review Checklist

## Inline Comments

- [ ] Comments explain **why**, not what — if "what" is needed, code itself is unclear (suggest rename/refactor or split functions)
- [ ] Exception: complex algorithms / regex / tricky business logic — detailed "what" comments or links to docs are acceptable
- [ ] No stale comments around changed code: outdated info, resolved TODOs, contradicting-behavior comments removed

## API Docs

- [ ] New/changed public methods/endpoints have docs: usage rules, params, expected responses, error cases
- [ ] OpenAPI/Swagger spec updated if API contract changed
- [ ] AsyncAPI spec updated if API contract changed

## README & External Docs

- [ ] README updated if build/run/test/deploy steps changed
- [ ] New env vars, DB settings, config files documented with up-to-date info
- [ ] High-level docs (esp. new projects) understandable by non-technical reader / newcomer
- [ ] Docs for removed/deprecated functionality also removed or marked deprecated

## Module & Class Docs

- [ ] New classes/methods/modules have macro-level docs: purpose, use cases, dependencies
