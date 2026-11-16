---
name: advanced-elicitation
description: "Find blind spots in your own plan, design or decision: fresh subagents run critique methods (pre-mortem, red team, expert panel) as cold readers, then you debate their findings and revise. Use before you execute a plan, before you finalize a design or choice that is costly to undo, when you pick between options, after the same approach failed twice, or when asked for advanced elicitation."
triggers:
  - "advanced elicitation"
  - "blind spots"
  - "stress-test the plan"
  - "critique my plan"
  - "pre-mortem"
---

# Advanced Elicitation

Your first plan is your most likely plan: centered on the first idea, agreeable with its own reasons. You cannot see its blind spots, because you hold every reason behind it. A **cold reader** can: a fresh subagent that gets the target and a critique method, and none of your reasons. You run cold readers, debate their findings, and continue the task with the revised target.

## 1. Check the stake

Run this skill when one of these is true:
- you wrote a plan of 3 or more steps and execution has not started
- the next action, or the plan or design you are about to finalize, is costly to undo: DB schema or migration, public API or DTO, data deletion, new dependency, architecture, deploy
- you choose between 2 or more workable options
- the same approach failed twice and you are about to try again
- the user or the task asks for it

A step that one command can verify and git can undo goes straight to execution.

## 2. Stage the target

Make a work folder `/tmp/elicit/<slug>/`; `<slug>` is a short kebab-case name for the target. Write `target.md`:

```markdown
# Target: <one line>
Kind: plan | decision | approach | retry
Repository: <absolute path, or none>

<the plan steps, numbered; or the decision: the options and the one you chose>
```

Put **what** you will do in `target.md`, never **why**. Your reasons anchor the reader; the target must stand on its own.

Then write the **settled** list: one line each, only what the user or the task fixed (stated constraints, user decisions, required tools or vendors). Your own choices are not settled; they are what the readers test.

## 3. Pick the methods

Find the target's row. Run push 1 and push 2. Add push 3 for a plan of 5 or more steps or an action that cannot be undone.

| Target | Push 1 | Push 2 | Push 3 |
|---|---|---|---|
| Execution plan | Pre-mortem | Assumption Audit | Problem Decomposition |
| Choice between options | Steelmanning | Second-Order Thinking | Question the Question |
| Code, API or schema design | Failure Mode Analysis | Expert Panel | Subtraction |
| Action that cannot be undone | Cascading Failure | Assumption Audit | Edge Case Sweep |
| Security or access change | Red Team | Assumption Audit | Failure Mode Analysis |
| Large or growing plan | Subtraction | Pre-mortem | Assumption Audit |
| Retry after failure | 5 Whys | Assumption Audit | Explain Reasoning |

Each method has a **direction** in [`references/methods.md`](references/methods.md); every push of a round comes from a different direction. A target that fits two rows takes push 1 of each row; when the two share a direction, the second row gives its next push instead. A round has at most 3 pushes: more readers repeat each other and cost more than they find. Read `references/methods.md` now: copy each chosen method's gist and form line exactly into its brief.

## 4. Brief and dispatch

Give each push its own fresh subagent, all at once, all against the same `target.md`. Read [`references/spawning.md`](references/spawning.md) for the call syntax of your runtime. Each brief is this text with the placeholders filled, and nothing more: no opinion, no reasons, no other push's result.

```text
You are a cold reader. You did not write the target and you owe it nothing.
Run one critique method on it.

Target: /tmp/elicit/<slug>/target.md
Purpose: <one line: what the target must achieve, and for whom>
Settled, do not reopen:
- <one line each, or "none">
Method: <name>. <gist>
Form: <form line>

You may read files and run read-only commands (rg, ls, cat, git log, git show) to check a claim.
Edit nothing. Run nothing that changes state. Spawn no agents.

Return text in this shape, findings first:
## Findings
F1 | severity: blocker or major or minor | where: <step number or line> | problem: <what is wrong or missing> | change: <the exact edit to the target>
At most 5 findings, worst first, one line each. Each finding is specific to this target: a finding that fits any plan of its kind is noise.
"No findings." is a valid result.
## <method name>
<the form, sized to the target, at most 15 lines>
```

Save each return verbatim as `/tmp/elicit/<slug>/r<round>-<method>.md`: the push file holds the reader's text, never yours. A return in the wrong shape goes back to the same reader (see `references/spawning.md`) with `Return your findings in the shape of the brief.`; save its new return verbatim.

**Expert Panel** is one push with 2 or 3 voices. Pick each voice from a field the target touches: database, security, API consumer, operations, UI, domain. Each voice gets its own subagent and its own brief, with this line after `Form:`:

```text
Role: you are a senior <field> expert. Read the target only from this field.
```

The voices never see each other. Save each return as `r<round>-panel-<field>.md`.

## 5. Debate the findings

Give every finding one verdict:
- **ADOPT**: the finding stands. This is the default.
- **REJECT**: only with a **ground**: (a) it contradicts a settled item, name it; (b) evidence you checked shows it is wrong, quote `file:line` or command output; (c) it is outside the task, quote the task line. "Unlikely", "fine in practice" and "adds complexity" are not grounds: those findings are ADOPT.
- **ESCALATE**: the finding attacks the premise: the goal, the user's request, or a settled item.

A finding that asks for several changes gets one verdict per change, logged as `F<n>a`, `F<n>b`.

Rebut once. Send each reader its REJECTED blocker and major findings with your grounds, in the same subagent (see `references/spawning.md`):

```text
I reject these findings. For each one, reply CONCEDE, or HOLD with new evidence (file:line, command output, or a concrete failure scenario).
F<n>: <ground>
```

CONCEDE closes the finding. HOLD with new evidence turns it into ADOPT or ESCALATE. HOLD without new evidence stays REJECT. One exchange, then the verdicts are final.

## 6. Revise

Edit `target.md` with every ADOPT change. For each ESCALATE:
- the user can answer now: ask, with the finding and your recommended answer
- you run autonomously: take the option that keeps more choices open (reversible, smaller, behind a flag), continue, and list the escalation in your final response

## 7. Second round

Run a second round when the revision adopted a blocker or changed the target's structure (switched option; added, removed or reordered a step). Use one method from a direction not used yet, against the revised `target.md`, in a fresh subagent; save its return as `r2-<method>.md`, then debate and revise as in steps 5 and 6. Add round 1 results to the settled list: each adopted change as settled, each rejected finding as "rejected: <one line>". Keep round 1 findings out of the brief so the reader stays cold.

Stop after round 2. A blocker still open after round 2 goes into your final response.

## 8. Log and continue

Write `/tmp/elicit/<slug>/log.md`, one row per finding, the push file named exactly:

```markdown
# <target one line>
| ID | Push file | Severity | Verdict | Ground or change | Rebuttal |
|---|---|---|---|---|---|
| F1 | r1-pre-mortem.md | major | REJECT | (b) app.py:12 already retries | CONCEDE |
| F2 | r1-pre-mortem.md | blocker | ADOPT | step 3: back up users.db first | - |
Escalations: <one line each, with the option you took>
```

Then run the check from this skill's folder:

```bash
python3 <skill folder>/scripts/check.py /tmp/elicit/<slug>
```

Each `FAIL` line names the file and the fix. Fix, then run it again. The skill is done when the check prints `OK`, every ADOPT is in `target.md`, and every ESCALATE is asked or listed.

Continue the task with the revised `target.md` as your plan. Add to your final response: methods run, changes adopted, escalations, path of the work folder.
