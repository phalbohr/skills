# Harnesses

How the coordinator spawns workers, sends messages, and sets model and effort. Find your harness by the tools you have. If a tool refuses a call, use the next fallback in the same section.

## Claude Code desktop app

Tools named `mcp__ccd_session__*` and `mcp__ccd_session_mgmt__*`. Load deferred ones with ToolSearch.

- Spawn: `start_session` with `initiation: "user_asked"`, `context: "fresh"`, `use_worktree: false` for a shared working copy, a `name`, the tier `model`, the first task `effort`, the brief as `prompt`, and the plan doc path and team rules in `background`.
- Model: `set_session_model`. Effort: `set_session_effort`. Read back with `get_session` (`model`, `effort`).
- Limits: a worker gets the coordinator's model family or a cheaper one, and the coordinator's effort or lower, without a prompt. Run the coordinator on the strongest model at `max`. A higher effort or model makes the app ask the user (effort gate step 4).
- Send a task: `SendMessage` with `to` set to the worker's `local_…` id.
- Reports arrive as cross-session messages. Worker states: `list_sessions` with `linked: true`.
- Fallback: `set_session_effort` refused → effort gate step 4, the user changes effort in the session's model menu.

Effort levels: `low`, `medium`, `high`, `xhigh`, `max`.

## Codex

Multi-agent tools such as `spawn_agent`, `send_input`, `wait`, `close_agent`.

- Spawn: `spawn_agent` with the brief. Pass `model` and `reasoning_effort` when the tool schema has them.
- A new effort for the next task, when the tool cannot change it on a live agent: close the agent and spawn a new one with the new effort. Give it the plan doc path and the last accepted state, so it starts warm.
- Fallback: no per-agent model or effort in the schema → define agent roles in `~/.codex/config.toml` (`[agents.<role>]` with a config file that sets `model` and `model_reasoning_effort`), one role per tier and effort, after the user approves the config change.
- Reports: the agent's final message, read with `wait`.

Effort levels: `minimal`, `low`, `medium`, `high`, `xhigh`. Map the plan doc levels to this scale once, in the plan doc.

## Separate sessions the user opens

No spawn tool, or the user prefers to open sessions by hand.

- Write each worker's first message to a file and give the user the path, the model and the effort for each session.
- The user relays messages, or the workers write reports to an agreed file that the coordinator reads.
- Effort gate step 4 always applies.
