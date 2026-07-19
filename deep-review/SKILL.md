---
name: "deep-review"
description: "Conducts deep code review following 13 specialized instructions. Creates structured reports with critical issues, risks, and recommendations."
version: "3.1.0"
author: "Agent Zero Team"
tags: ["code-review", "quality", "security", "deep-analysis"]
trigger_patterns:
  - "deep review"
  - "deep code review"
  - "conduct deep-review"
---

# Deep Review Skill

## When to Use

Activate this skill when the user requests a deep code review of one or more files.

---

## Overview: Map-Reduce Architecture

This skill uses a three-phase Map-Reduce pattern to ensure quality and avoid repeated work:

- **Phase 0 (Map):** Main agent loads all project context and instruction files **once**, classifies files, builds a Project Map, and performs cross-file analysis.
- **Phase 1 (Tier A):** Main agent runs cross-file reviews across all files simultaneously.
- **Phase 2 (Reduce):** Sub-agents perform per-file reviews in **parallel**, each receiving the Review Package (Project Map + relevant instructions) as text in their prompt — **no disk re-reads**.
- **Phase 3:** Main agent assembles the final report.

---

## Phase 0: Setup

### Step 1 — Collect Files

Accept one file or a list of files as `[files-to-review]`. If not provided, ask the user.

### Step 2 — Determine Output Folder

Accept an optional output folder path as `[output-dir]`. If not provided, **explicitly ask the user** where to save the report. There is no default — the path must be provided by the user. Store the resolved path as `OUTPUT_DIR` for all subsequent steps.

### Step 2 — Load Project Context (once)

Read all of the following **before** any review work begins. **Follow all references or includes found within them recursively** (e.g., if `GEMINI.md` references `rules/openapi-guide.md`, read that file too):

- `GEMINI.md` (if exists)
- `CLAUDE.md` (if exists)
- All files referenced/linked from the above
- `skills/deep-review/instructions/01-arch-design-review.md`
- `skills/deep-review/instructions/02-functionality-reliability-review.md`
- `skills/deep-review/instructions/03-secure-code-review.md`
- `skills/deep-review/instructions/04-performance-review.md`
- `skills/deep-review/instructions/05-test-review.md`
- `skills/deep-review/instructions/06-clean-code-review.md`
- `skills/deep-review/instructions/07-style-automation-review.md`
- `skills/deep-review/instructions/08-documentation-review.md`
- `skills/deep-review/instructions/09-nitpick-review.md`
- `skills/deep-review/instructions/10-logging-security-review.md`
- `skills/deep-review/instructions/11-logging-review.md`
- `skills/deep-review/instructions/12-logging-error-handling-review.md`
- `skills/deep-review/instructions/13-log-retention-review.md`
- `skills/deep-review/templates/report-format.md`
- `skills/deep-review/templates/report-template.md`

Also read all files in `[files-to-review]` and their direct imports/dependencies.

### Step 3 — Classify Files (Smart Routing)

For each file, determine its type and the applicable Tier B review categories:

| File Type | Applicable Tier B Steps |
|-----------|------------------------|
| Source code (`*.java`, `*.py`, `*.ts`, `*.go`, etc.) | All (Functionality through Log Retention) |
| Config / IaC (`*.xml`, `*.yml`, `Dockerfile`, terraform files) | Secure Code, Log Retention, Nitpick |
| Test files (`*Test*`, `*Spec*`, files in `test/` or `__tests__/`) | Functionality, Clean Code, Nitpick, Documentation |
| Documentation (`*.md`, `*.rst`) | Documentation, Nitpick |

Record the classification in the Project Map.

### Step 4 — Build Project Map

Write a compact Project Map into the report file as an appendix. This artifact is passed as text to all sub-agents — they do not re-read project docs from disk.

The Project Map must include:
- **Project rules** — mandatory requirements extracted from `GEMINI.md`/`CLAUDE.md` and ALL files they reference, as a flat bullet list: "Project requires: X" (distilled, not raw prose)
- **Critical Exceptions** — any rule marked as "Critical Exception", "MUST", "NEVER", or "Always" in project docs must be **copied verbatim** (do not paraphrase). These override common industry standards and must survive distillation intact.
- **Architecture** — layers, module boundaries, key conventions (naming, structure, tooling)
- **Banned patterns** — anything explicitly forbidden in project docs
- **Files under review** — one-line description of each file's role (inferred from name, package, first ~30 lines)
- **File dependencies** — explicit import/dependency relationships between reviewed files
- **Test infrastructure** — test framework, coverage tooling, test directory structure
- **Routing table** — which Tier B steps apply to each file (output of Step 3)

### Step 5 — Create Report File

- **Single file:** `${OUTPUT_DIR}/deep-review-[filename].md` with header:
  ```
  # Deep Review Report
  **Date:** [current_date]
  **File reviewed:** [filename]
  ```
- **Multiple files:** `${OUTPUT_DIR}/deep-review-[current_date]-multi.md` with header:
  ```
  # Deep Review Report
  **Date:** [current_date]
  **Files reviewed:** [list of all files]
  **Mode:** Multi-file (Map-Reduce)
  ```

---

## Phase 1: Cross-File Analysis (Tier A)

Perform these reviews yourself with **all files in context simultaneously**. Tag findings as `[filename:line]`.

### Step 6 — Project Standards Compliance

Review all files together against the project rules in the Project Map.

**CRITICAL: Project-specific rules and Critical Exceptions override general industry knowledge.** If a file follows a project-specific exception (even if it looks non-standard), mark it as compliant — do NOT flag it as an issue.

**Report section:** `## 00-project-standards-compliance`

| Level | Examples |
|-------|---------|
| CRITICAL | Code directly contradicts a mandatory project rule or Critical Exception |
| RISK | Violates a named convention or architecture decision from project docs |
| ADVISORY | Minor deviation from style or patterns described in project docs |

> Use only what is **explicitly stated** in project docs. Generic best practices are covered by Tier B steps.

### Step 7 — Architecture & Design Review

Review all files together against `instructions/01-arch-design-review.md`. Focus on cross-file concerns: coupling, layer violations, duplicated functionality.

**Report section:** `## 01-arch-design-review`

| Level | Examples |
|-------|---------|
| CRITICAL | Fundamental architectural flaws, broken layered design, tight coupling of core modules |
| RISK | SOLID principle violations, incorrect design patterns, mixed responsibilities |
| ADVISORY | Poor module organization, minor architectural inconsistencies |

### Step 8 — Test Coverage Mapping

Identify which implementation files have corresponding test files and which do not. Record a coverage map (used by sub-agents in Phase 2).

**Report section:** `## 05-test-coverage-map`

Format:
```
| File | Test File | Coverage Status |
|------|-----------|-----------------|
| FileA.java | FileATest.java | ✅ Found |
| FileB.java | — | ❌ No test file |
```

---

## Phase 2: Per-File Reviews (Tier B)

### Sub-Agent Policy

If your environment supports delegating tasks to sub-agents (e.g., via `generalist` tool in Gemini CLI, `Agent` tool in Claude Code, Sub-tasks in Kilo Code, or equivalent in other platforms), you **MUST** spawn parallel sub-agents for Phase 2 — one per file. Pass the Review Package directly in the sub-agent prompt.

If no sub-agent tool is available, fall back to sequential per-file processing within the main session. Acknowledge this limitation in the report header.

Platform examples (informational):
- **Gemini CLI** → `generalist` subagent, launch all simultaneously
- **Claude Code** → `Agent` tool, `subagent_type: "general-purpose"`, all calls in a single message
- **Kilo Code** → New Task, launch simultaneously
- **Unknown / Antigravity** → agent chooses the mechanism or uses sequential fallback

### Sub-Agent Prompt Template

For each file, spawn a sub-agent with this prompt (fill in all placeholders):

```
You are a Senior Software Engineer conducting a focused code review.

## Project Map
[INSERT full Project Map text here]

## MANDATORY RULE: PROJECT PRECEDENCE
The Project Map above is the absolute source of truth for this codebase.
**Project-specific rules and Critical Exceptions ALWAYS override your general training knowledge or industry best practices** (e.g., standard Spring, OpenAPI, or React conventions).
If the Project Map states an exception (e.g., "routing annotations MUST stay in Controller, never Interface"), treat it as an inviolable rule.
Flagging code that follows a project-specific exception as an issue is a hallucination — do NOT do it.

## Cross-File Findings (context only — do not duplicate these in your output)
[INSERT key findings from Phase 1 here]

## Test Coverage Map
[INSERT test coverage map from Step 8 here]

## File to Review
**Path:** [file path]

[INSERT full file content here]

## Review Instructions

Apply the following review categories in order.
For each category, append a `###` heading and record findings using this exact format:

[INSERT full contents of report-format.md here]

Do NOT fix any issues — only report them.
Stay in realistic scope for a small to medium-sized app.
Do not suggest optimizations for hypothetical high-load scenarios.

## Categories to Apply
[INSERT only the instruction files applicable to this file per Smart Routing]

[INSERT relevant instruction file contents here — only the ones from Smart Routing]

## Severity Reference
Use exactly 3 levels: CRITICAL (🔴) / RISK (🟡 Potential risks) / ADVISORY (🔵 Recommendations).
See the severity table in the "Review Step Protocol" section of this skill.

CRITICAL: Return ONLY the raw Markdown sections starting directly with the first `###` heading.
Do not include any conversational filler, greetings, summaries, or conclusions.
```

### Fault Tolerance

If a sub-agent fails or returns no result:
- In the per-file section: write `> ⚠️ Review failed due to sub-agent error.`
- In the Summary table: mark the file with status `ERROR`
- Continue with remaining files — do not abort the entire review

---

## Phase 3: Finalize Report

### Step 9 — Assemble & Verify Report

Insert all sub-agent outputs into the report under `## Per-File Analysis` (for multi-file) or directly (for single file).

**Before finalizing:** scan all sub-agent findings against the Project Map. If any finding flags behavior that the Project Map explicitly permits (a project-sanctioned Critical Exception), remove that finding from the report.

### Step 10 — Write Summary

**Single file:** summary table identical to current format (backward compatible):
```
## Summary
| Severity           | Count   |
| ------------------ | ------- |
| 🔴 Critical        | [count] |
| 🟡 Risks           | [count] |
| 🔵 Recommendations | [count] |

**Total issues found:** [total]
```

**Multiple files:** combined table at the top of the report:
```
## Summary

### Cross-File Issues
| Severity           | Count   |
| ------------------ | ------- |
| 🔴 Critical        | [count] |
| 🟡 Risks           | [count] |
| 🔵 Recommendations | [count] |

### Per-File Totals
| File | 🔴 Critical | 🟡 Risks | 🔵 Recs | Status |
|------|------------|---------|---------|--------|
| FileA.java | N | N | N | ✅ |
| FileB.java | N | N | N | ERROR |

**Total issues found:** [total]
```

### Step 11 — Finalize

- Make report as concise as possible; sacrifice grammar for brevity
- Ensure report complies with `templates/report-template.md`
- For multi-file: move Summary section to the top, before Cross-File Analysis

---

## Review Step Protocol (for sub-agents)

Each Tier B review step follows this protocol:

1. Review the file against the rules in the specified instruction file.
2. Append a `###` section heading to the output.
3. Record found issues using the format from `report-format.md` with exactly 3 severity levels (see below).
4. **DO NOT fix any issues — only report them.**
5. Skip steps marked "Not applicable" in the routing table (e.g., Log Retention for non-config files).

### Tier B Severity Levels

Use exactly **3 levels** matching `report-format.md`: CRITICAL (🔴), RISK (🟡), ADVISORY (🔵).

**Functionality & Reliability (`02-functionality-reliability-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Logic errors causing incorrect behavior, unhandled exceptions, broken core flows |
| RISK | Unhandled edge cases, race conditions, potential data corruption, missing timeouts |
| ADVISORY | Inefficient state management, suboptimal method structures, minor UI/UX bugs |

**Secure Code Review (`03-secure-code-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | SQL injections, XSS, unauthorized access, exposed secrets, RCE |
| RISK | Insecure cryptography, missing CSRF protection, excessive data exposure, missing rate limiting |
| ADVISORY | Missing security headers, insecure cookies, outdated dependencies with low-risk CVEs |

**Performance Review (`04-performance-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | O(n²) algorithms on large datasets, memory leaks, deadlocks, blocking IO |
| RISK | N+1 database queries, synchronous external calls in critical paths, missing caching |
| ADVISORY | Unoptimized indexes, large payloads, suboptimal use of collections |

**Test Review (`05-test-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Missing tests for core logic, tests passing with broken code |
| RISK | Flaky tests, testing implementation details, missing edge cases |
| ADVISORY | Repetitive test setup, unclear assertions, minor naming issues |

**Clean Code Review (`06-clean-code-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Unreadable spaghetti code, massive God classes, extreme cyclomatic complexity |
| RISK | Heavy code duplication (DRY), magic numbers/strings, highly misleading naming |
| ADVISORY | Overly long methods, excessive parameters, dead code, unused imports |

**Style & Automation Review (`07-style-automation-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Bypassing CI/CD pipelines, broken build scripts, syntax errors failing build |
| RISK | Ignoring mandatory linter warnings, missing CI checks |
| ADVISORY | Inconsistent formatting, non-standard naming conventions, disorganized imports |

**Documentation Review (`08-documentation-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Missing public API docs, dangerously incorrect documentation |
| RISK | Outdated README, missing setup steps, lacking architecture diagrams |
| ADVISORY | Unclear method signatures, undocumented hacks, typos in comments |

**Nitpick Review (`09-nitpick-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Confusing typos or naming that change meaning of code |
| RISK | Inconsistent naming patterns causing significant cognitive load |
| ADVISORY | Extra whitespace, trailing spaces, spelling in comments, missing EOF newline |

**Logging Security Review (`10-logging-security-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Logging passwords, tokens, API keys, or raw PII |
| RISK | Logging full HTTP payloads with sensitive headers |
| ADVISORY | Logging session IDs or internal IDs unnecessarily, minor inconsistencies in security log tags |

**Logging Review (`11-logging-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Missing logs for critical functionality, swallowing exceptions |
| RISK | Wrong log levels (ERROR for expected flow), noisy logs masking issues |
| ADVISORY | Missing context (user ID, transaction ID), unstructured text logs, typos in log messages |

**Logging & Error Handling Review (`12-logging-error-handling-review.md`)**
| Level | Examples |
|-------|---------|
| CRITICAL | Application crashing without error logs, broken error recovery |
| RISK | Leaking stack traces to end-users, empty catch blocks |
| ADVISORY | Vague error messages, inconsistent API error responses, generic exceptions instead of specific ones |

**Log Retention Review (`13-log-retention-review.md`)** — apply only to config/IaC files
| Level | Examples |
|-------|---------|
| CRITICAL | Indefinitely storing logs without rotation causing disk exhaustion |
| RISK | Missing log rotation mechanisms, excessive retention of DEBUG logs |
| ADVISORY | Unoptimized log aggregation, missing TTLs, inconsistent log file naming |

---

## Backward Compatibility

- Single-file input: Phase 0+1 works as before (one sub-agent, no "Per-File Analysis" wrapper)
- Report section numbering (00–13): unchanged
- Single-file report format: identical to previous versions

---

## TODO: Diff-Mode (future)

Accept `git diff` output alongside file list. Sub-agents focus on changed lines, use full file as context only. Useful for PR reviews to avoid noise from pre-existing issues.

---

## Usage Examples

### Example 1: Single File with Output Folder

**User:** "Conduct deep-review for @src/main/java/UserService.java, save to /tmp/reviews/"

**Agent:**
> Loading project context...
> Building Project Map...
> Running cross-file analysis (single file mode)...
> Spawning sub-agent for UserService.java...
> Assembling report...
>
> ✅ Report: `/tmp/reviews/deep-review-UserService.java.md`

### Example 2: Multiple Files (Output Folder Asked)

**User:** "Deep review: UserService.java, UserController.java, logback.xml"

**Agent:**
> To conduct a deep review, I need to know where to save the report.
> Where should I save it?

**User:** "/tmp/reviews"

**Agent:**
> Loading project context (once)...
> Classifying files: 2 source + 1 config...
> Building Project Map...
> Running cross-file analysis...
> Spawning 3 parallel sub-agents...
> Assembling combined report...
>
> ✅ Report: `/tmp/reviews/deep-review-2026-01-15-multi.md`

### Example 3: No Files Provided

**User:** "Need to do deep-review"

**Agent:**
> To conduct a deep review, please specify:
> 1. Which file(s) to review?
> 2. Where to save the report?

---

## Tips

- Always load full project context before any review
- Avoid false positives — check neighboring files and imports when context is unclear
- Write the report in English
- Use diff blocks for code examples
- Prioritize critical issues in the summary
