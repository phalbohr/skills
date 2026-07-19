# AI Code Style Conventions Guide

## Table of Contents

1. [Variable Declarations](#1-variable-declarations)
2. [Class Purpose Documentation (CPUD)](#2-class-purpose-documentation-cpud)
3. [Imports vs FQN](#3-imports-vs-fqn)
4. [Nested Idempotency Keys](#4-nested-idempotency-keys)
5. [No Magic Values](#5-no-magic-values)
6. [Test Naming (@DisplayName)](#6-test-naming-displayname)
7. [Test Zero Comments Policy](#7-zero-comments-policy)

## 1. Variable Declarations

**ALWAYS** use `var` for local variable declarations when the type is obvious. Reduce visual noise. Do not use explicit types unless required for clarity. Example: `var list = new ArrayList<String>();`.

**EXCEPTION — unconstrained generic return types:** Do NOT use `var` when the call site is the sole source of type inference for an unconstrained generic (e.g. `<T> T processOperation(...)`). Java infers `Object` in that case, causing a compile error. Use the explicit return type instead:
```java
// WRONG — R infers to Object, ResponseEntity<Object> ≠ ResponseEntity<MassStockResponse>
var response = service.processOperation(request, userId);

// CORRECT
MassStockResponse response = service.processOperation(request, userId);
```

## 2. Class Purpose Documentation (CPUD)

Keep PRODUCTION classes extremely clean from text boilerplate. All classes must follow an absolute **Zero Comments Policy** (no JavaDoc, no class-level comments).

## 3. Imports vs FQN

ALWAYS use `import`. Avoid fully-qualified class names (FQN) inline unless resolving a naming collision (e.g. `java.util.Date` vs `java.sql.Date`).

## 4. Nested Idempotency Keys

No parent key reuse. Derive nested keys: `UUID.nameUUIDFromBytes((parentKey + ":" + opId).getBytes(UTF_8))`. Suffix `opId` MUST be unique per sub-op type.

## 5. No Magic Values

No magic numbers, strings, or other literals in logic. Extract every non-obvious constant to a named `static final` field. The name must explain _what_ the value represents, not restate the value itself. Example: `PAGINATION_PARAMS = Set.of("page", "size", "sort")` — callers understand intent without reading the literal.

## 6. Test Naming (@DisplayName)

- **Class:** `@DisplayName("[ClassName] Tests")`
- **Method:** `@DisplayName("[Condition] - should [expected behavior]")`

## 7. Test Zero Comments Policy

Tests MUST be self-documenting. Absolutely NO comments inside test methods (no "what/why", no TODOs). Extract complex setups into private helper methods instead of explaining them with text.
