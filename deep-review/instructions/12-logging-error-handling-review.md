# Logging & Error Handling Review Checklist

## Exception Swallowing & Presence

- [ ] No empty `catch` blocks — every caught exception must be handled or logged
- [ ] `try-catch` blocks do real work — not silently swallowing exceptions
- [ ] If exception intentionally ignored: comment explains why it's safe + log at TRACE/DEBUG level

## Exception Specificity

- [ ] No bare `catch (Exception e)` — catch specific types (IOException, TimeoutException, etc.)
- [ ] try-catch logs match actual exception type; no blind catch-all without distinguishing error cause
- [ ] Different exception types handled separately with appropriate logic and log messages

## Exception Logging Quality

- [ ] Error messages are informative enough for future debugging (e.g. including business context, failing input params)
- [ ] Exception object `e` passed to logger — not just `e.getMessage()` (stack trace must be preserved)
- [ ] Full stack trace logged on unexpected failures, not just message or internal hints
- [ ] Log message includes business context: user ID, transaction ID, or failing input params

## Graceful Degradation & Correctness

- [ ] After caught error: system continues working if possible (fallback/default behavior, no crash)
- [ ] Logic doesn't silently fail; terminal states reachable
- [ ] Log level is correct (ERROR for terminal failure, WARN for recovery/fallback)
