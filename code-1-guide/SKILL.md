---
name: code-1-guide
argument-hint: [путь/к/File.java | описание задачи]
description: >
  Java/Spring Boot production code conventions for this project. ALWAYS apply when:
  creating or editing any Java or Kotlin production file (not tests, docs, or config),
  writing new classes/services/controllers/repositories/entities/mappers/operations/DTOs,
  or working in any src/main directory. Do NOT apply for src/test/, *.md, *.yml, *.yaml,
  *.properties, build scripts, or config files.
paths: "**/src/main/**"
---

# Production Code Conventions

Apply every rule below when writing or editing Java/Kotlin production code (files under `src/main/`).

---

## 1. Technical Text Language

All developer-facing text (comments, logs, exceptions, APIs, tests) MUST be in English.

## 2. Optimistic Locking

Mutable `@Entity` classes must declare `@Version`. Use the object wrapper `Long` or `Integer` (not primitive `long`) to ensure JPA `save()` handles the "new entity" lifecycle correctly via `null` checks. Do NOT map the column explicitly (`@Column` is forbidden).

## 3. @Transactional, @Retryable, and @Idempotent

**STRICT LAYERING REQUIRED:**

- **Inner Operation:** `@Idempotent` + `@Transactional` (atomic logic).
- **Outer Service:** `@Retryable` ONLY. Must call the inner operation so each retry opens a fresh transaction.
- **Read-Only Service:** `@Transactional(readOnly = true)`.
  **CRITICAL:** NEVER combine `@Retryable` and `@Transactional` on the same method.

**Propagation type selection:**

Default to `REQUIRED`. Pick another value ONLY if its row matches exactly; when two rows seem to fit, the more specific scenario wins.

| Scenario | Propagation |
|---|---|
| Standard business logic (default) | `REQUIRED` |
| Read-only helper | `SUPPORTS` |
| Part of a larger operation | `MANDATORY` |
| Audit / logging / email | `REQUIRES_NEW` |
| Heavy read-only / bulk | `NOT_SUPPORTED` |
| External HTTP, TX forbidden | `NEVER` |
| Partial rollback with continuation | `NESTED` |

**Decision order:** TX forbidden (external HTTP) → `NEVER`. Must run isolated from caller's TX (audit/log/email) → `REQUIRES_NEW`. Must already be in a TX → `MANDATORY`. Read-only → `SUPPORTS` (or `NOT_SUPPORTED` for heavy/bulk). Otherwise → `REQUIRED`.

**Trap — REQUIRED + catch:** `inner()` marks TX `rollback-only` → `outer()` gets `UnexpectedRollbackException` on commit even if exception was caught. Fix: use `REQUIRES_NEW` for `inner()`.

**Trap — self-invocation with REQUIRES_NEW:** Calling from the same bean bypasses Spring AOP proxy → new TX is NOT created. Fix: extract to a separate bean.

## 4. Fail-Fast Principle

Place ALL guard clauses and parameter validations at the absolute top of the method before business logic.

## 5. Tell, Don't Ask Principle

Business logic mutates state INSIDE domain objects. Call `stock.decreaseQuantity(x)` on entities. Do not extract state into the service to make decisions externally.

## 6. Strict Layering: Reads/Writes via Service

ALL database access (reads and writes) MUST go through the Service (or UseCase/Query) layer to encapsulate business constraints, security, and filtering in one place. Controllers or other presentation components MUST NEVER access Repositories directly.

## 7. API Boundaries & Object Passing

You MAY pass whole objects (DTOs, Entities) intra-service to avoid the "Long Parameter List" anti-pattern. However, you MUST NEVER pass complete entity/domain objects across inter-service API boundaries (use strict integration DTOs instead).

## 8. Single Responsibility Principle (SRP)

Classes/methods must have exactly ONE reason to change.

## 9. JPA Persistence Best Practices

When saving entities, ALWAYS capture and use the instance returned by `repository.save()`. Discard the original object reference to avoid detached entity bugs.

## 10. Single Level of Abstraction

High-level methods must read like a narrative. Bury implementation details inside small, descriptively-named private methods.

## 11. Layer Responsibilities

- **Controller:** Validates input (`@Valid`), delegates to Service, builds DTO HTTP response. NO logic, NO repos.
- **Service:** Orchestration (when Operations are used). Throws domain exceptions directly (e.g. `EntityNotFoundException`).
- **Operation:** Atomic business logic. Annotated `@Idempotent` + `@Transactional` (see rule 3).
- **Mapper:** Isolated conversion logic only. No business rules, no side effects.
- **CRITICAL:** Controllers MUST NOT perform `null` checks on service responses to determine HTTP 404s. `GlobalApiExceptionHandler` must handle domain exceptions and map to status codes.

## 12. Layer Dependency Rules

Dependencies flow INWARD. The domain layer must be framework-free.

- NO `org.springframework.web.*` in the domain.
- Domain exceptions are plain `RuntimeException` subclasses without HTTP mapping annotations.
- HTTP mapping belongs to `GlobalApiExceptionHandler`.

## 13. Backend vs Frontend Boundary

**Strict Layer SRP:** Backend = business logic, auth, domain data. Frontend = UI, formatting (dates/i18n), presentation. NEVER leak frontend presentation concerns into backend APIs. NEVER leak backend business rules into frontend execution. Solve problems ONLY in their native domain.

## 14. Principle of Least Privilege

Grant the narrowest access that works. Widen only when a real caller needs it.

- **Members:** default `private`. `protected` only for intended subclass extension, package-private for same-package collaborators, `public` only for the declared API.
- **Classes:** package-private unless used outside the package. Prefer `final` (Java) / non-`open` (Kotlin) by default.
- **State:** fields `private final`. No setters for invariant-bearing state — mutate via domain methods (see rule 5). No exposing internal collections; return unmodifiable copies.
- **Variables:** declare in the narrowest scope that works. No field where a local suffices, no method-wide variable where a block-local suffices.
- **Data exposure:** DTOs carry ONLY the fields the caller needs. Never expose internal ids, hashes, or audit fields "just in case".
- **Read-only intent:** query endpoints and methods are declared read-only (`@Transactional(readOnly = true)`, `GET` without side effects).
- **Tests:** NEVER relax a modifier or add a getter just to test. Test through the public API.
- **Roles/security:** authorize at the Service/Operation layer, deny by default. Assign the minimal role/scope per endpoint; no wildcard roles. Service accounts and DB users get only the rights they use (no shared admin credentials).
- **Config/secrets:** mount a secret only into the service that uses it. ENV carries no unused variables.
