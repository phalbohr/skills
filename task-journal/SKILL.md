---
name: task-journal
description: "Writes a detailed educational journal entry about a completed task. Use this whenever the user wants to document, explain, or post-mortem work done in the current session — phrases like 'напиши отчёт', 'write a journal', 'документируй задачу', 'создай отчёт о задаче', 'task report', 'разбери что мы делали', 'объясни что мы изменили'. The skill synthesizes the session into a narrative that explains not just WHAT changed, but WHY — suitable for onboarding, knowledge transfer, or personal learning. Accepts a file path as argument."
version: "1.0.0"
tags: ["journal", "documentation", "post-mortem", "learning", "onboarding"]
---

# Task Journal Skill

Create a detailed educational journal entry that explains a completed task from first principles — what it was, why it was needed, what changed, what broke, what was learned. The goal is a document that a developer unfamiliar with the codebase could read and fully understand.

---

## Input

The user provides a file path as the argument to `/task-journal`:

```
/task-journal .gemini/journal/TICKET-123-my-task.md
/task-journal /absolute/path/to/report.md
```

If no path is given, ask the user where to save the report.

---

## How to extract information from the session

The conversation history is already in your context. Work through it to answer these questions:

**About the task:**
- What was the user trying to accomplish? What was the ticket/branch/goal?
- Why did this task need to happen at all? What was the problem or business need?
- What was the state of the code before the task began?

**About the changes:**
- What files were modified, created, or deleted?
- For each group of related changes: what was the old approach, what is the new approach, and why was the change necessary?
- Were there any non-obvious constraints that shaped the implementation?

**About problems encountered:**
- What failed during the task (test failures, compile errors, unexpected behavior)?
- What was the root cause of each failure?
- How was each problem diagnosed and fixed?

**About concepts:**
- What are the key technical concepts involved that a reader would need to understand?
- Are there any "gotchas" or counterintuitive things that became clear during the task?

---

## Report structure

Write the report in Markdown. Use this structure, adapting section titles and depth to what actually happened:

```
# <Ticket/task name> — <short description>

**Branch/PR:** ...
**Date:** ...

---

## 1. Why this task was needed

[Explain the business or technical problem. Not what changed — WHY change was needed at all.
Include historical context: why was it built the previous way? What assumption changed?]

## 2. How the old approach worked

[Explain the mechanism being replaced or modified. Assume the reader is smart but unfamiliar.
Use concrete examples: show the old code/config and explain what it did.]

## 3. What changed and why

[One subsection per logical group of changes, not per file.
For each group: show before/after if helpful, explain the reasoning.]

### 3.1. [Change group name]
...

### 3.2. [Change group name]
...

## 4. Problems encountered

[For each non-trivial problem: what the symptom was, what the root cause turned out to be,
how it was diagnosed, and the fix. This section is especially valuable for learning.]

## 5. Summary of changed files

[Table: file path | what changed | why]

## 6. Key concepts and lessons

[1–5 technical concepts the reader needs to understand this task.
Explain each one clearly, with examples from the task. Focus on transferable knowledge —
things that apply beyond this specific ticket.]
```

---

## Writing guidelines

**Language: always Russian.** The entire report — headings, explanations, code comments — must be in Russian, regardless of what language the session was conducted in. Technical terms (Jackson, ObjectMapper, @JsonProperty) stay in their original form but everything else is Russian.

**Write for a complete beginner.** Assume the reader is an intelligent person who has never seen this part of the codebase, may not know the framework deeply, and wants to truly understand — not just see a changelog. If a concept appears that a beginner might not know (e.g. "naming strategy", "Spring bean", "anonymous class"), explain it briefly right there in the text. Don't say "as you know" — assume they don't know.

**Explain the WHY at every level.** The most valuable part of a journal entry is the motivation, not the mechanics. Why did this configuration exist in the first place? Why did removing it break tests? Why is one ObjectMapper different from another? If a reader understands the reasoning, they can adapt it to new situations. If they only know what was done, they can only copy it.

**Be concrete and verbose.** Show actual code snippets with before/after. Quote exact error messages. Describe what you see in the browser/terminal. Abstract descriptions evaporate; concrete examples stick. When in doubt, include more detail, not less.

**Narrate, don't list.** Prose is easier to learn from than bullet points. Write flowing paragraphs that tell the story of the task, not a dry changelog. Use analogies where they help ("this is like...").

**Sections 4 and 6 are the most important.** The problems section captures the diagnostic thinking that would otherwise disappear forever — how you noticed something was wrong, what you investigated, what turned out to be the actual cause. The concepts section teaches transferable knowledge. Spend extra effort on these two sections.

---

## After writing

Tell the user the path where the report was saved and offer a one-line summary of what was documented.
