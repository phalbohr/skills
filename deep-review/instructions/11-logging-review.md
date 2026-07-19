# Logging Review Checklist

## Strategic Logging

- [ ] No "captain obvious" logs (e.g. `log.info("Entering method X")`) — remove if value-free
- [ ] No logging inside intensive/hot loops — aggregate and log once after loop, or log errors only
- [ ] Correct log levels: DEBUG/TRACE for variable values/intermediate state; INFO only for significant business events
- [ ] No duplicate logging of same error across layers (e.g. service + controller both logging same exception with stacktrace)
- [ ] Messages are specific: state **what** action failed and **why** (e.g. `log.error("Failed to update user profile: DB timeout")`)

## Context Completeness

- [ ] Correlation/Request/Session IDs attached to every log entry — enables full request trace across microservices
- [ ] Key metadata present: user ID (no PII), env, method name, timestamp
- [ ] Critical events (login attempts, access changes, transactions) logged with enough detail for security investigation

## Performance

- [ ] Parameterized logging used instead of string concat: `log.debug("{} loaded {} bytes", user, size)`
- [ ] No heavy object/collection serialization solely for logging (large objects, full API responses)
- [ ] In high-load contexts: logging doesn't cause thread pool exhaustion via I/O blocking
- [ ] Expensive ops needed only for log message wrapped in `if (log.isDebugEnabled()) { ... }`
- [ ] Logging volume doesn't degrade performance
