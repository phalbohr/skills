# Test Review Checklist

> Start review with test code — tests serve as documentation and build mental model before reading impl.

---

## 1. Presence & Types

- [ ] Every new feature / logic change has new or updated tests **in the same PR**
- [ ] Even pure refactors are covered (verify behavior unchanged)
- [ ] Correct test type chosen: unit / integration / e2e
- [ ] Multi-component changes → integration tests present
- [ ] Coverage meets team threshold (e.g. 80% lines, expressions, branches)

## 2. Test Validity (Will they actually fail?)

- [ ] Tests **would fail** if production code breaks
- [ ] Tests verify real use cases, not just inflating coverage %
- [ ] Assertions are simple, clear, meaningful
- [ ] Tests are not brittle (no false positives on safe code changes)

## 3. Edge Cases & Negative Paths

- [ ] Not limited to happy path only
- [ ] Boundary conditions covered
- [ ] Unexpected / failure scenarios covered
- [ ] Error generation and error handling tested

## 4. Readability & Maintainability

- [ ] Test code meets same style/quality standards as production code
- [ ] No over-complex test logic (if hard to read fast → not good enough)
- [ ] Complex tests don't add tech debt instead of catching bugs
- [ ] Concurrent code: tests don't share race-prone resources (e.g. shared `java.util.Random` across threads)
- [ ] Concurrent code: tests are capable of detecting concurrency bugs

## 5. CI/CD Integration

- [ ] New tests are wired into CI/CD pipeline
- [ ] Pipeline blocks merge if tests fail
- [ ] Pipeline blocks merge if coverage drops below threshold
