# Code Documentation Guide

## Table of Contents

1. [Interface-Driven Documentation (Hybrid Split)](#1-interface-driven-documentation-hybrid-split)
2. [Global Errors](#2-global-errors)
3. [@ParameterObject](#3-parameterobject)
4. [JSR-303 Validation](#4-jsr-303-validation)
5. [OpenAPI Documentation Constants](#5-openapi-documentation-constants)
6. [External YAML ($ref)](#6-external-yaml-ref)
7. [Generic Response Schemas (e.g. PageResponse<T>)](#7-generic-response-schemas-eg-pageresponset)
8. [Database Schema Documentation](#8-database-schema-documentation)

## 1. Interface-Driven Documentation (Hybrid Split)

Keep controllers clean. Use Hybrid Split Interface-Driven Documentation:

Extract all OpenAPI annotations to an `XxxxApi` interface. Controller implements the interface. Use `therapi-runtime-javadoc` to pull descriptions from JavaDoc — minimizes annotation noise.

- **Interface:** `@Operation`, `@ApiResponses`, `@ApiResponse`, `@Parameter`, `@Tag`.
- **Controller:** `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`, `@RequestMapping`, `@RequestParam`, `@RequestBody`, `@PathVariable`, `@Valid`, `@PreAuthorize`.

**CRITICAL — Routing:** ALL Spring MVC routing and security annotations MUST remain in the Controller. Required for reliable request mapping and `@WebMvcTest`/`MockMvc` compatibility.

## 2. Global Errors

**Rule:** Declare an error response in the API interface **only if it carries endpoint-specific information** (e.g., a 400 caused by filter-parameter validation with a distinct description). Errors that add no extra meaning beyond what `GlobalApiExceptionHandler` already documents (e.g., a generic 401 Unauthorized or 403 Forbidden) **must not** be repeated in the interface.

## 3. @ParameterObject

**Rule:** Group more than 2 query parameters into a DTO and use `@ParameterObject` in the **Interface** signature to expand fields in Swagger UI. `Pageable` is supported automatically.

## 4. JSR-303 Validation

**Rule:** Do not manually describe constraints in `@Schema`. SpringDoc automatically reads `@NotNull`, `@Min`, `@Max`, `@Size`, etc., from your DTOs.

## 5. OpenAPI Documentation Constants

**Rule:** If an `@Operation` description must explain non-trivial caller rules (filter syntax, operators, value formats), extract it to a `final` constants class in `application/controller/openapi/` and reference it from the Api interface. Simple one-line descriptions stay inline.

- Naming: `<Domain>OpenApiDocumentation` / `<OPERATION>_DESCRIPTION`
- Every such class requires a `*OpenApiDocumentationTest`: private-constructor test + not-null/blank assertion per constant. See `InventoryOpenApiDocumentation` + its test as the reference.

## 6. External YAML ($ref)

**Rule:** For very large documentation blocks, use external YAML files in `src/main/resources/static/*.yaml` and link them via `$ref`.

## 7. Generic Response Schemas (e.g. PageResponse<T>)

**Rule:** To correctly generate generic schemas (e.g. `PageResponse<T>`), omit the `content = @Content(...)` block entirely in `@ApiResponse(responseCode = "200")`. This allows Springdoc to accurately infer the generic types from the method signature.

## 8. Database Schema Documentation

**Rule:** Every table, column and enum type in a Flyway migration carries a `COMMENT ON`, and so does every CHECK constraint and partial unique index that encodes a business rule. Read from the database alone, the comment tells why the object exists, which principle and decision it follows, which scenarios need it, and how its name is meant. This documentation is mandatory; the Zero Comments Policy does not cover it.

**Sources**, read before writing. itemis-shop paths are relative to `itemis-shop-docs/specs-alternative/analysis/04-hybrid/`:
- `datenmodell-felder.json`: purpose (`zweck`), rules (`regel`, `regeln`) and scenarios (`szenarien`) per table and field; the `entfallen` list names columns that will be removed and their replacement.
- `entscheidungen.md`: principles P1–P9 and decisions H1–H35.
- `szenarien.md`: scenarios S (own) and T (team spec).
- `itemis-shop-docs/architecture/development-plan/hybrid-zielmodell/umsetzungsplan.md`: decisions E, where the implementation deviates from or adds to H.

An object the documentation does not describe gets a comment derived from its migration and the code that writes it, and is listed as a documentation gap in the summary.

**Template** (English, like all developer-facing text):

```sql
COMMENT ON TABLE <schema>.<table> IS
'One row = <what one row is>.
Purpose: <which question or process needs it; what breaks without it>.
Source: <source of truth | derived from <table>, checked by <query>>.
Written by: <the only write path>. Read by: <screens, services>.
Lifecycle: <when a row appears, what changes, deleted or never deleted>.
Not: <what is NOT stored here and where it is instead>.
Rules: <P…, H…, E…>. Scenarios: <S…, T…>.';

COMMENT ON COLUMN <schema>.<table>.<column> IS
'<What the value is: unit, currency, time zone, sign>.
NULL: <what NULL means>.
Values: <range, or every enum value with its meaning>.
Set by: <who and when; immutable after …>.
Not: <the likely misreading and the correct field>.
Rules: <…>. Scenarios: <…>.';
```

Example:

```sql
COMMENT ON COLUMN inventory_v2.holdings.closed_at IS
'Time the loan was finished: everything returned, lost or written off.
NULL: the loan is open.
Set by: StockLedger when open_quantity reaches 0.
Not: the return time. Each return, also a partial one, is a holding_returns row with its own returned_at.
Rules: H17. Scenarios: S5, S29.';
```

**Content:**
- The first sentence says what one row or one value is. Rule and scenario IDs stand next to the explanation, never in its place.
- `NULL:` on every nullable column; `Values:` on enums, statuses, quantities and ranges; `Not:` on every name a reader can misread.
- Enum types list every value with its meaning.
- Cross-service id: `<Service> id, no FK.`
- Column that will be removed: `LEGACY: removed in <step>. Replacement: <…>. New code must not read or write it.`
- Deviation from the target model: `Deviates from H…: <what>. Decision E….`
- The comment states the current meaning only: change history, TODOs and names of people stay out.
- Comment and documentation agree; a contradiction is resolved by fixing one of the two.

**Placement:**
- A migration that is not yet on the target branch (`develop`) gets the comments inside itself.
- A migration already on the target branch is immutable (Flyway checksum): its comments go into a new migration.
- A migration that existing databases skip (the baseline version under `baseline-on-migrate`) gets its comments in the next migration; otherwise they never reach production.

**Coverage test:** each service has one Postgres integration test (Testcontainers) that runs all migrations and expects zero rows from this query; its failure message lists the rows. Replace `<schema>`; for `public` also exclude `flyway_schema_history` in both table filters.

```sql
SELECT t.table_name, NULL AS column_name
  FROM information_schema.tables t
 WHERE t.table_schema = '<schema>' AND t.table_type = 'BASE TABLE'
   AND obj_description(format('%I.%I', t.table_schema, t.table_name)::regclass, 'pg_class') IS NULL
UNION ALL
SELECT c.table_name, c.column_name
  FROM information_schema.columns c
  JOIN information_schema.tables t
    ON t.table_schema = c.table_schema AND t.table_name = c.table_name AND t.table_type = 'BASE TABLE'
 WHERE c.table_schema = '<schema>'
   AND col_description(format('%I.%I', c.table_schema, c.table_name)::regclass, c.ordinal_position) IS NULL
UNION ALL
SELECT ty.typname, NULL
  FROM pg_type ty
  JOIN pg_namespace n ON n.oid = ty.typnamespace
 WHERE n.nspname = '<schema>' AND ty.typtype = 'e'
   AND obj_description(ty.oid, 'pg_type') IS NULL;
```
