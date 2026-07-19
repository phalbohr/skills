# Clean Code & Simplicity — AI Review Checklist

## 1. KISS / General Readability

- [ ] Requires multiple re-reads to follow logic → red flag, suggest simpler alternative
- [ ] Over-engineered? (unnecessary abstractions/generalization beyond current needs) → flag, redirect to solving _now_ problem only
- [ ] Would another engineer easily understand and modify this in 6 months?

## 2. Complexity (3 levels)

- [ ] **Lines:** No horizontal scrolling needed to read a single line
- [ ] **Functions/Methods:** Functions compact? Complex logic broken into small, digestible pieces?
- [ ] **Classes:** Classes not overloaded with responsibilities and dependencies?

## 3. Naming

- [ ] Names clearly describe what the variable/function/class does — no `x`, `temp`, etc.; prefer `userAge`, `totalPrice`
- [ ] Length balanced: not overly verbose, not abbreviated to obscurity
- [ ] Consistent with team conventions (e.g. camelCase, snake_case) and coherent across similar concepts project-wide
- [ ] Similar concepts named consistently across the project; no unjustified abbreviations

## 4. DRY (Don't Repeat Yourself)

- [ ] Repeated code blocks that could be extracted into reusable functions/classes?
- [ ] Could existing project libraries or built-ins replace newly written logic?

## 5. Comments & Documentation

- [ ] Comments explain **why**, not what (decision rationale, non-obvious business logic)
- [ ] Comment explains _what_ code does → code should be simplified to be self-documenting instead
- [ ] Complex/tricky algorithms have detailed explanations or links to relevant docs/papers
- [ ] Stale, redundant, or code-repeating comments → remove
- [ ] New modules or public APIs added → README/API docs updated?
