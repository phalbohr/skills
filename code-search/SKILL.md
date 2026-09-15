---
name: code-search
description: "How to search and understand an unfamiliar codebase cheaply — routing between ast-grep (structural), graphify (relationships), and reading files. Use BEFORE the first Read/grep of any code question: where is X, who calls X, what breaks if I change X, how does this system fit together, which part handles Y. Also covers keeping a graphify graph fresh and its artifacts from flooding context."
---

# Code search routing

Three tools, three jobs. Pick by question shape, not by habit.

| Question | Tool |
|---|---|
| Where is X defined / who calls X / all code matching a shape | **ast-grep** — structural, no regex false positives, milliseconds |
| What does X touch / what breaks if I change X / how do X and Y connect | **graphify** — traverses real + inferred edges; grep cannot do reverse deps |
| Which part of the system handles Y | **graphify wiki/report**, grepped — never read whole |
| Anything else about specific lines | **Read**, last, only files you will edit |

ast-grep beats graphify on single-symbol lookups by an order of magnitude. graphify wins
only where structure alone can't answer: reverse dependencies, inferred relationships,
and the map of what-lives-where. Use both; don't substitute one for the other.

## Token safety — the part that actually decides whether this saves or costs

graphify writes artifacts whose size scales with the repo. On a large graph the report
alone can exceed 100 000 tokens. **Never Read a graphify artifact blind.**

Check first, then choose:

```bash
wc -c graphify-out/GRAPH_REPORT.md graphify-out/wiki/index.md 2>/dev/null
```

- Over ~40 KB → do not Read it. Grep a slice: `sed -n '/^## Import Cycles/,/^## /p' …`
  Report section anchors: `## Summary`, `## Community Hubs`, `## God Nodes`,
  `## Surprising Connections`, `## Import Cycles`, `## Communities`.
- `wiki/index.md` is a link list of every community → grep it for a domain keyword to
  find the right area, then Read that **one** article. This two-step is the cheapest
  possible entry point into an unknown repo and should be the default first move.
- `graph.json` is never Read, catted, or piped into context. CLI only.
- Piping bulk output through `ctx_execute` keeps it out of context when you only need a
  count or a filtered subset.

```bash
# callers of a method (any language ast-grep supports)
ast-grep run --pattern '$OBJ.methodName($$$)' --lang <lang> <dir>
# structural search with a rule; $$$ = any number of nodes
ast-grep scan --inline-rules 'id: r
language: <lang>
rule:
  pattern: class $N implements TargetInterface { $$$ }' <dir>
# when a pattern will not match, inspect the real node kinds
ast-grep run --pattern '<snippet>' --lang <lang> --debug-query=ast <dir>
```

## Commands worth knowing

```bash
graphify explain "Symbol"            # file:line, degree, every edge — the workhorse
graphify affected "Symbol" --depth 2 # reverse dependencies; irreplaceable
graphify god-nodes --top 20          # architectural hubs, cheap overview
graphify path "A" "B"                # needs BOTH exact node names
```

Every call re-parses the whole graph (seconds on a large repo). Batch your questions;
never call `explain` in a loop.

`graphify query "<sentence>"` is the weak tool: entity matching seeds the traversal from
loose word matches, then truncates to the token budget and warns that the answer may be
in what it cut. Pass an exact symbol name, narrow with `--context`, and if it truncates
switch to `explain` rather than raising `--budget` — an unbudgeted traversal can cost
hundreds of thousands of tokens.

## Keeping the graph fresh

`graphify hook install` puts a `post-commit` / `post-checkout` git hook in the repo that
rebuilds detached in the background — AST only, no LLM, no agent tokens. Verify with
`graphify hook status`; log at `~/.cache/graphify-rebuild.log`; bypass once with
`GRAPHIFY_SKIP_HOOK=1`. Run `graphify update .` by hand only for uncommitted work you
must query right now, and `GRAPHIFY_FORCE=1` after a refactor that deleted code.

To build a graph for the first time, or for doc/image/deep semantic extraction, invoke
the **`graphify` skill** — it owns the build pipeline. This skill only covers querying.

## Two traps that silently destroy graph quality

**Re-clustering is not reproducible.** `update` and `cluster-only` re-run community
detection; on a large graph the community count and ids shift between runs on identical
input. Community labels are keyed to membership signatures, so a shift makes graphify
revert the affected labels to raw hub symbols (`org.junit.jupiter.api.Test`) — largest
communities first, because they change membership most. To refresh a *view*, never
re-cluster: `graphify export wiki`, `graphify export html`, and `graphify tree` read the
existing graph and leave clustering alone.

**Labels need an LLM backend** (`gemini|kimi|claude|openai|deepseek|ollama|claude-cli`),
and `graphify label` is the only supported route. With no API key in the environment:

- A small local ollama model produces category words ("Microservices", "E-commerce")
  instead of architectural names — check output quality before trusting it.
- Any headless CLI agent works as a substitute labeller: batch the communities with
  their highest-degree members, ask for a 2–5 word capability name each, then write
  results into `.graphify_labels.json` **and** stamp `community_name` onto `graph.json`
  nodes by community id in place — that field is what `explain` reads. Do **not** run
  `cluster-only` afterwards, or the work is reverted.
- Verify a headless agent actually honours a structured-output flag; some ignore it and
  return plain text.

## Never do first

- `grep` to find a symbol → ast-grep
- Read files to understand architecture → grep `wiki/index.md`, read one article
- Read `GRAPH_REPORT.md` / `wiki/index.md` / `graph.json` whole → size-check, then slice
- Chains of `find`/`grep`/`cat` → one ast-grep scan, or `ctx_batch_execute`

## Subagents

Subagent prompts must carry these rules explicitly — name the tools and forbid reading
the large artifacts whole. A subagent that Reads the report spends the parent's budget.
