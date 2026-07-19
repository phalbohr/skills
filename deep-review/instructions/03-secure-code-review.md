# Security Code Review Checklist

> Adopt adversarial mindset. Focus on data flows, trust boundaries, and logic flaws that automated scanners miss.
> Automate the obvious (SAST/DAST for injection syntax, secret scanning, CVEs). Spend human/AI review time on architecture, trust boundaries, and complex business logic.

---

## 1. Injection & Input Validation

- [ ] SQL: parameterized queries / prepared statements only — no string concatenation in SQL
- [ ] XSS: all user input sanitized; output escaped before rendering in browser
- [ ] All inputs (user, external systems, 3rd-party APIs) validated for correct type, length, and value range

## 2. Access Control & Authorization

- [ ] Least privilege: users/services granted minimum required rights; OAuth2/OIDC and RBAC correctly applied
- [ ] IDOR: direct object access by ID (e.g. `/user/123`) verifies that the authenticated user owns/is authorized for that record — or uses non-guessable tokens instead

## 3. Authentication

- [ ] No weak or default passwords in use
- [ ] Brute-force & credential stuffing protection present: rate limiting, CAPTCHA, and/or MFA

## 4. Cryptography & Sensitive Data

- [ ] No hardcoded secrets (passwords, API keys, tokens) in source code or committed config files (e.g. `.env`) — automated secret scanning preferred
- [ ] Passwords hashed with bcrypt / scrypt / Argon2 + salt — MD5 / SHA-1 not acceptable
- [ ] Data in transit uses TLS/HTTPS; sensitive data at rest encrypted (e.g. AES-256)

## 5. SSRF & Dependencies

- [ ] User-supplied URLs strictly validated before server makes outbound requests — internal resources must not be reachable
- [ ] New 3rd-party libraries checked for known CVEs and active maintenance status (Snyk / Dependabot recommended)
