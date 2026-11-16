# Critique methods

Each method has a **direction**: the kind of blind spot it hunts. Copy the gist and the form line exactly into the brief.

| Direction | Hunts |
|---|---|
| wrong | errors inside the target |
| missing | what the target does not cover |
| premise | a wrong problem or a wrong starting point |
| simplify | excess, and parts that do not need to exist |
| future | how the target fails over time or under change |
| other-side | the strongest case against the target |

## wrong

- **Edge Case Sweep.** Try the extremes: empty, zero, maximum, malformed, concurrent, the inputs happy-path thinking skips. Form: a table of boundary inputs and what the target does with each, failures marked.
- **Failure Mode Analysis.** For each part, how it fails and what that takes down. Form: one line per component: failure, effect, how it is detected, how it is prevented.
- **Consistency Check.** Restate the target's claims and find where it contradicts itself, its own numbers, or the code. Form: pairs of claims that conflict, with the one to keep and why.
- **Explain Reasoning.** Show the steps from premise to conclusion and find where one does not follow. Form: the reasoning step by step, each step marked as given, inferred or asserted, the asserted ones challenged.

## missing

- **Assumption Audit.** List every assumption, rate it, stress the weakest. Form: a table of assumptions rated for confidence and impact, then the three weakest stress-tested against the repository or the facts.
- **Second-Order Thinking.** Follow each consequence to the consequence it causes. Form: for each action: the first-order effect, what that effect causes next, what to do about it.
- **Expert Panel.** Experts from the fields the target touches read it, each alone, each only from their own field. Form: one expert's reading from their field: what they see, what concerns them, and the change each concern calls for, located in the target.
- **Stakeholder Lens.** Each party the target affects (user, caller, consumer module, operator, future maintainer) says what it owes them. Form: one stakeholder at a time in their own voice for a few lines, then what the target owes them, located in the target.

## premise

- **Question the Question.** Ask whether the stated problem is the real problem. Form: the stated problem, the better problem, and what the target becomes if it solves that one.
- **First Principles.** Strip the assumptions and rebuild from what is known to be true. Form: the assumptions stripped, the truths that remain, the approach rebuilt from them, and where it differs from the target.
- **5 Whys.** Ask why until the root cause, not the symptom, is in hand. Form: the chain of whys, five deep, ending at the root cause and what changes because of it.
- **Abstraction Laddering.** Move up for why and down for how, then pick the altitude. Form: the target restated one level up and one level down, and which altitude it should sit at.

## simplify

- **Subtraction.** Improve by removing, against the habit of adding. Form: what to remove, one line each with what is lost and gained, then the leaner target.
- **Problem Decomposition.** Split the whole into parts that can be solved and verified alone. Form: the independent parts, the order to build and verify them, and where the target's split differs.
- **Feynman Technique.** Explain it simply; every stall is a gap. Form: the target explained to a smart twelve-year-old, every place the explanation stalls marked as a gap.

## future

- **Pre-mortem.** Assume it failed; explain why. Form: written from after the failure: what went wrong, in order, and what in the target made it likely.
- **Cascading Failure.** Break one thing on purpose and trace where the break travels. Form: one failure triggered, its path through the dependencies, the single points of failure named, and what hardens each.
- **What If Scenarios.** Put the target in situations it did not plan for. Form: three scenarios the target did not plan for, and how it fares in each.
- **Inversion.** Ask what would guarantee failure, then avoid it. Form: a recipe for guaranteed failure, then what the target must do to avoid each step.

## other-side

- **Steelmanning.** Build the case for the strongest option the target did not choose, at full strength, before answering it. Form: the opposing case argued as its best advocate would, then only what honestly survives.
- **Red Team.** Attack it as an adversary would, then harden it. Form: an attacker's plan against the target, step by step, then the hardening for each step.
- **Socratic Questioning.** Question until the target cannot answer. Form: a chain of questions, each answered from the target, until one it cannot answer.

Adapted from the BMAD-METHOD advanced elicitation catalog (MIT).
