# Code Documentation Guide

## Table of Contents

1. [Interface-Driven Documentation (Hybrid Split)](#1-interface-driven-documentation-hybrid-split)
2. [Global Errors](#2-global-errors)
3. [@ParameterObject](#3-parameterobject)
4. [JSR-303 Validation](#4-jsr-303-validation)
5. [OpenAPI Documentation Constants](#5-openapi-documentation-constants)
6. [External YAML ($ref)](#6-external-yaml-ref)
7. [Generic Response Schemas (e.g. PageResponse<T>)](#7-generic-response-schemas-eg-pageresponset)

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
