# Performance, Readability & Maintainability Guide

## 1. Performance

- No N+1 queries — fetch related data via JOIN or eager loading, not per-iteration queries
- No DB or external API calls inside loops
- New SQL queries target indexed fields — no full table scans
- No unnecessary loops — prefer stream/batch operations where possible
- Large collections processed in chunks or streams, not loaded entirely into memory
- Frequently repeated DB/external-service calls have a caching layer
- Algorithmic complexity justified — flag O(n²)+ where a better alternative exists

## 2. Readability

- Names clearly describe what the variable/function/class does — no `x`, `temp`, `data`
- Name length balanced: not verbose, not abbreviated to obscurity
- Functions/methods are small and focused — one level of abstraction per method
- No magic numbers — replace with named constants
- Comments explain **why**, not what — if "what" is needed, simplify the code instead
- Complex algorithms or non-obvious business rules have a short explanation
- HTTP method semantics match standards — deviations changed or documented

## 3. Maintainability

- DRY — no repeated logic blocks that could be extracted into reusable functions
- No dead code, no commented-out code left in production
- No unnecessary complexity or speculative abstractions (YAGNI)
- Proper separation of concerns — no method doing more than one job
- Code is modular: new components general enough for future reuse without over-engineering
- Breaking changes documented; technical debt explicitly noted
