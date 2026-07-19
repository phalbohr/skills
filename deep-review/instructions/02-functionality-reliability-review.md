# Functionality & Logic Reliability Checklist

## 1. Intent & User Value

- [ ] Implementation satisfies all acceptance criteria from the task/user story
- [ ] Behavior is useful — for end users OR for devs consuming this code

## 2. Edge Cases

- [ ] Handles: `null`, empty lists, zero-length strings, unexpected types
- [ ] **MANDATORY:** If a method uses fields from a DTO/Record parameter (e.g., `fr.field()`, `fr.operator()`) without explicit null checks, you **MUST** read the DTO/Record class definition.
    - Check if the fields carry `@NotNull`, `@NotBlank`, or other constraints.
    - If the DTO has no such validation annotations, flag the missing check as **🔴 CRITICAL (CIA: Availability)**.
- [ ] No off-by-one errors in array traversal; no integer overflows
- [ ] All edge cases covered by unit/integration tests

## 3. Error Handling & Logic

- [ ] After caught error: system continues working if possible (fallback/default behavior, no crash)
- [ ] Logic doesn't silently fail; terminal states are reachable and correct

## 4. Concurrency

- [ ] **Race conditions:** shared mutable state accessed from multiple threads protected by synchronization (`synchronized`, locks, `volatile`, atomic types, or immutable data)
- [ ] **TOCTOU (Time-of-Check-Time-of-Use):** check-then-act sequences (e.g. `if exists → use`) are atomic — not split across unsynchronized steps
- [ ] **Deadlocks:** multiple locks acquired in consistent order across all code paths; no circular lock dependency (A→B in one path, B→A in another)
- [ ] **Starvation:** low-priority threads not permanently blocked by high-priority ones; lock hold time is minimal
- [ ] Concurrent collections used where appropriate (`ConcurrentHashMap`, `CopyOnWriteArrayList`) instead of manual synchronization on regular collections
- [ ] `CompletableFuture` / reactive chains: exceptions handled at each stage — unhandled rejections don't silently swallow errors
