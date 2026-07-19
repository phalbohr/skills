# Performance Review Checklist

## 1. Algorithmic Complexity

- [ ] Evaluate Big O (time & space) for loops and recursion — flag O(n²)+ where avoidable (e.g. bubble sort → better alternative)
- [ ] Correct data structure for the job — e.g. HashMap over ArrayList for frequent lookups

## 2. Database Efficiency

- [ ] No N+1: related data fetched via eager loading or JOIN, not per-iteration queries
- [ ] No DB/API calls inside loops
- [ ] New SQL queries target indexed fields — no full table scans
- [ ] DB connections closed and resources released properly

## 3. Memory & Resource Management

- [ ] Large objects/collections processed in chunks or via streams where possible
- [ ] No excessive object retention or duplicate processing (→ memory leaks)
- [ ] Mobile: memory usage doesn't cause abnormal battery drain

## 4. Caching & Concurrency

- [ ] Frequently repeated DB/external-service calls have caching layer
- [ ] Threads used only where justified — no CPU overload, no unnecessary locks

## 5. Frontend (if applicable)

- [ ] Minimal unnecessary component re-renders
- [ ] Event handlers use debounce/throttle where needed; heavy assets are optimized

## 6. Tooling & Automation

- [ ] CI/CD pipeline includes static analysis / profiling (e.g. SonarQube) to catch perf issues, slow queries, memory leaks, and high-latency ops pre-production
