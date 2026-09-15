---
name: post-mortum
description: "Writes a post-mortem report about problems and mistakes that occurred during the current session — what went wrong, why, and how to avoid it next time. Use this whenever the user asks to document session problems, lessons learned, or process improvements: 'создай пост-мортем', 'напиши что пошло не так', 'write a post-mortem', 'document mistakes', 'что можно было сделать лучше', 'разбери ошибки сессии'. Accepts a file path as argument. Focuses on process failures, wrong tool choices, missed clarifications, and produces universal questions/instructions that prevent the same mistakes on any future task."
version: "1.0.0"
tags: ["post-mortem", "retrospective", "process", "learning", "improvement"]
---

# Post-Mortem Skill

Analyse the current session for process failures, missed clarifications, wrong choices, and unexpected obstacles. Write a post-mortem report that is useful not just for this task — but as a reference for any future programming session.

---

## Input

The user provides a file path as the argument to `/post-mortum`:

```
/post-mortum .gemini/post-mortem/TICKET-123-post-mortem.md
/post-mortum /absolute/path/to/report.md
```

If no path is given, ask the user where to save the report.

---

## What to look for in the session

Go through the conversation history and find every moment where things did not go smoothly. Cast a wide net — include not just hard failures but also inefficiencies, corrections, and misunderstandings.

**Process failures:**
- Were the wrong tools used? (e.g. grep instead of ast-grep, cat instead of a proper code navigator)
- Were important files read multiple times because state was lost?
- Did the session stall waiting for information the AI should have asked for upfront?

**Scope and clarification failures:**
- Did the user have to correct the direction mid-task?
- Were there constraints or exclusions (files not to touch, services not to break) that only became clear after work started?
- Was the impact radius of the change underestimated?

**Technical surprises:**
- Did tests fail unexpectedly? Were the failures predictable in hindsight?
- Did a configuration change have side effects that were not anticipated?
- Was there a hidden dependency that only surfaced at runtime?

**Communication failures:**
- Did the AI respond in the wrong language?
- Were responses too verbose or too terse for what the user needed?
- Did the AI make assumptions that turned out to be wrong?

**Environment / tooling failures:**
- Were there permission issues, isolation guards, missing tools, or broken commands?
- Did the session have to be interrupted for a manual fix the AI should have flagged upfront?

---

## Report structure

```
# Post-mortem: <Ticket/task name> — <short description>

**Ветка/задача:** ...
**Дата:** ...

---

## Проблема N: <short name>

**Что случилось:** [One paragraph — what actually happened, concrete and specific]

**Почему это плохо:** [Why this cost time, introduced risk, or degraded output quality]

**Вопрос, который помогает:**
> [A question to ask at the START of a session that would have prevented this.
>  Word it broadly — it should work for any programming task, not just this one.]

**Инструкция:**
> [A concrete instruction for Claude or a project's CLAUDE.md that prevents recurrence.
>  Again, keep it general enough to apply across projects.]

---

## Универсальный чеклист вопросов перед любой задачей

[Group the questions from above into categories.
 These should be phrased as standalone questions a developer could read before starting any task.
 Categories: Скоуп и границы / Тесты и верификация / Риски и откат / Инструменты и контекст]

---

## Универсальные инструкции для CLAUDE.md

[A ready-to-paste block of markdown instructions that the user can add to their CLAUDE.md
 to prevent the problems documented above from recurring in future sessions.
 Make these practical and concise — they should not require reading the full post-mortem to understand.]

---

## TL;DR

[3 questions or instructions that alone would have prevented the majority of problems in this session.
 Short enough to memorise.]
```

---

## Writing guidelines

**Language: Russian.** The entire report is in Russian. Technical terms (Jackson, ObjectMapper, SNAKE_CASE, CLAUDE.md) stay in their original form.

**Be specific first, then generalise.** Each problem section starts with exactly what happened in this session — a concrete incident, not a vague observation. Then the question and instruction are generalised so they work for any future session.

**The question and instruction are the deliverable.** The incident description explains why the question matters. The question and instruction are what the user will actually use. Invest in making them precise, actionable, and broadly applicable. A question like "Есть ли части системы, которые нельзя трогать?" is worth including in every session; a question like "Нужно ли удалять аннотацию @JsonProperty?" is not.

**Prioritise problems that were non-obvious.** Every session has small hiccups. Focus on the problems where a reasonable developer would have made the same mistake — these are the ones worth capturing. Skip trivial typos or one-off environment glitches.

**The CLAUDE.md block should be copy-pasteable.** Write it as valid Markdown that the user can paste directly into their project's CLAUDE.md without editing. Use second-person imperative directed at Claude.

**Scale to what actually happened.** If the session had two real problems, write two sections — don't pad. If there were six distinct failures, write six. Quality over completeness theatre.

---

## After writing

Tell the user the path where the report was saved and offer a one-line summary of what was documented.
