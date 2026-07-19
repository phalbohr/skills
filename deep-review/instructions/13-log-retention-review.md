# Log Retention & Storage Architecture Review

## 1. Retention Period

- [ ] Logs retained long enough for incident investigation
- [ ] Min retention ≥ 6 months (cyberattacks often discovered late; root cause analysis requires historical data)

## 2. Compliance

- [ ] Reviewer aware of app's domain/industry
- [ ] Financial/payment apps: audit logs retained ≥ 1 year (PCI DSS or equivalent)
- [ ] If PR changes audit trail logic: data routed to long-term/cold storage, NOT a temporary cache

## 3. IaC & Config Inspection

- [ ] If PR touches server/container/logging configs (Terraform, CloudWatch, logrotate, Fluentd, ELK): check retention/rotation params
- [ ] Log rotation limits (size-based or time-based) won't cause data loss during peak load or DDoS (when log volume spikes drastically)

## 4. Immutable Storage

- [ ] Log storage is append-only by design
- [ ] App has no delete/modify permissions on its own log store (attacker compromising app cannot erase logs to cover tracks)
