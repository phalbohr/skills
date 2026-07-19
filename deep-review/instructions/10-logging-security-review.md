# Logging Security Review Checklist

## Sensitive Data in Logs

- [ ] No sensitive data in logs or user-facing errors (passwords, card numbers, session tokens, PII, DB connection strings, full file paths, system internals)
- [ ] No whole objects/payloads passed directly to logger (e.g. `log.info(userRequest)`) — objects may contain plaintext passwords, card numbers
- [ ] PII (names, emails, addresses, credit cards, record ownership) and PCI (financial data) masked/sanitized before logging; only non-sensitive fields (e.g. internal `userId`) are logged as-is
- [ ] Full request URLs not logged raw — sensitive params (session tokens, API keys, passwords) in URL must be excluded or masked
- [ ] App startup / config-loading logs don't expose DB credentials, certificates, connection strings, or hardcoded secrets

## Internal State Exposure

- [ ] Error messages: detailed info logged internally only (server-side), never returned to user in API response or UI — user sees generic message only (e.g. "An error occurred")
- [ ] `catch` blocks don't leak server file paths, directory structure, or DB paths to the outside
- [ ] No debug leftovers (`console.log`, `print`, `dump`) in production code
- [ ] Stack traces / raw exceptions / SQL exceptions stay inside internal monitoring only — never leak to external interfaces or untrusted third-party services
- [ ] Technical logs (vars, root cause) remain server-side; user-facing messages are generic
