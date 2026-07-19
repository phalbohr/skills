# Architecture & Design Review Checklist

## 1. High-Level Design & Context

- [ ] Does the new code integrate seamlessly — no duplicated functionality, no conflict with project goals?
- [ ] Does code comply with existing ADRs (Architecture Decision Records)?

## 2. SOLID Principles

- [ ] **SRP** — One class/module/function = one reason to change. No god objects.
- [ ] **OCP** — Behavior extendable without modifying existing source code?
- [ ] **LSP** — Subclasses fully substitutable for base class without breaking logic?
- [ ] **ISP** — Interfaces narrow and client-specific, not one large general-purpose interface?
- [ ] **DIP** — Dependencies on abstractions (interfaces), not concrete implementations?

## 3. KISS / No Over-Engineering

- [ ] Is the solution as simple as possible? No unnecessary complexity.
- [ ] Does it solve the _current_ problem only — no speculative generalization for hypothetical future scenarios?
- [ ] No unnecessary abstraction layers added without real benefit?

## 4. Modularity, Reuse & Coupling

- [ ] Loose coupling — no tight dependencies between unrelated modules?
- [ ] No reinventing the wheel — existing project utilities/libs could be reused?
- [ ] New components general enough for future reuse?

## 5. Design Patterns

- [ ] Appropriate team-approved patterns used (MVC, Repository, Factory, Observer, etc.)?
- [ ] Follows existing project conventions (error handling, DB access, etc.) for consistency?

## 6. Scalability, Reliability & Performance

- [ ] Does the architecture scale under high load?
- [ ] Is failure handled — external API down, DB offline, DDoS? Is the logic fault-tolerant?

## 7. Dependencies & Config

- [ ] No hardcoded config values, credentials, or parameters in source code?
- [ ] No dependency on obsolete/deprecated code or libraries scheduled for removal?
- [ ] No unnecessary third-party libs added when built-in language tools suffice?
