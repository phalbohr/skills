---
name: review-with-postman
description: Use when the user wants to review a merge request and generate Postman requests for the linked issue.
---

1. **Analyze MR**: Read the provided Merge Request URL.
   - *Completion criterion*: The linked closed issue number (e.g., `closes #...`) and the affected API endpoints are identified.

2. **Analyze issue**: Read the linked closed issue.
   - *Completion criterion*: The exact API requests needed to demonstrate the fix or feature are defined.

3. **Create folder**: Use the `postman` skill to create a folder named after the issue in the target Postman collection.
   - *Completion criterion*: The folder is successfully created in the target collection.

4. **Populate requests**: Use the `postman` skill to create the defined requests inside the new folder.
   - *Completion criterion*: Every request needed to demonstrate the issue's resolution is created in the folder.

## Hard-won rules (do not skip — these caused real failures)

- **Item IDs MUST be valid UUIDs.** When building the collection via `putCollection`, every `item`/folder `id` has to be a real UUID (e.g. `bb586b19-...`). Non-UUID strings like `pcs318-item-0001` are accepted by the API but the Postman desktop/web app silently refuses to render them — the folder shows up EMPTY even though `getCollection` returns all items. Generate ids with `uuid.uuid4()`.

- **Never write to collection variables from request test scripts.** Do NOT use `pm.collectionVariables.set(...)` to save created IDs. Writing a collection variable during a run mutates the collection model; the desktop app then persists its (possibly stale/empty) local copy back to the server and WIPES the requests you just pushed — symptom: "requests disappear after running the first one".
  - Instead: create a dedicated **Environment** (`createEnvironment`) holding all chained variables (`*Id`, `baseUrl`, `bearerToken`), and use `pm.environment.set(...)` in scripts. Running requests then never touches the collection.
  - Keep only read-only fallbacks (`pcsBaseUrl`, `bearerToken`) as collection variables; the selected environment overrides them.

- **After every `putCollection`, verify with `getCollection`** and confirm `itemRefs` contains the expected items. The server copy is the source of truth; the app view lags.

- **Tell the user to Pull, not restart.** If the collection was open before the push, the app holds a local copy. Restarting does not merge — instruct the user to **Pull changes** (right-click collection → Pull / sync ↻), and on conflict choose "pull / discard local", since the canonical version is the one just pushed.

- **`putCollection` silently drops `request.url` if you only send `{"raw": "..."}`.** The endpoint requires the full breakdown — `{"raw": ..., "host": [...], "path": [...], "query": [...]}` — otherwise it accepts the payload (200 OK) but persists `url.raw` as an empty string, and every request shows up with no URL. Always split the path into `host`/`path` segments (and `query` if there's a query string) when building requests for `putCollection`. `updateCollectionRequest` with a plain `url` string does NOT have this bug (it parses the raw string itself) — use it as a one-off patch, but never rely on it for bulk creation.

- **A variable reused across multiple stories/folders in the same collection MUST live at the collection level (`variable: [...]` in `putCollection`'s payload, or `createEnvironment`'s shared environment), not be reinvented per-folder.** Before adding a new fixture ID/base-URL/product-id variable, check whether another folder already owns a same-purpose variable — if the domain object differs (e.g. a UNIQUE_ITEM-nature product vs a MASS_STOCK-nature product), give it a distinct name (`imsTestProductAId` vs `imsTestProductId`), but if it's genuinely the same kind of shared fixture, reuse the existing collection/environment variable instead of creating a folder-local duplicate that only that folder's requests can see.

- **Before faking a field's value via direct create/PATCH, check whether it's actually settable that way.** DTOs are the source of truth for what's a legitimate request field — grep every controller/service that touches the entity for the *real* code path that sets a given field (e.g. `assignedUserId` is set by `PhysicalUniqueItem.issue()`, reachable only through a reserve → confirm-issuance flow, NOT through the create/update DTOs). If a field has no public setter, say so explicitly in the request's description instead of asserting it against a value you never actually drove non-null — a test that only checks "is null" without ever proving it was cleared from non-null is not testing the clearing behavior at all.

- **Before writing a status-transition chain, read the operation's transition `switch`/guard code — don't assume adjacency.** A domain status enum's states are not necessarily reachable from each other directly (e.g. `IN_STOCK` can only go to `DEFECTIVE`, never straight to `UNDER_REPAIR`). Trace every hop in a SETUP chain against the actual guard logic before writing the request sequence.

## Conventions to match existing review collections

- Collection-level `bearer` auth with token `{{bearerToken}}`.
- One folder per user story, named after the issue/US.
- Requests prefixed `[SETUP-n]` (preconditions that create fixtures + save their IDs) then `[AC-n]` (one per acceptance-criteria scenario, including negative/validation cases).
- Raw JSON bodies with a `Content-Type: application/json` header and `options.raw.language = json`.
- Add `pm.test(...)` assertions on the read-back requests so each AC is self-verifying.
- Base-URL variable per service (e.g. `pcsBaseUrl=http://localhost:8085`, `imsBaseUrl=http://localhost:8082`).
- JSON field names in request bodies default to camelCase (e.g. `idempotencyKey`, `productId`, `warehouseId`), matching this codebase's default Jackson config. Only use snake_case for a field/DTO that is explicitly `@JsonProperty`-annotated with a snake_case name in the source (check the DTO before writing the body — don't assume).
