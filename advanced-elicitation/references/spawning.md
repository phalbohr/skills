# Spawning cold readers

Find your runtime. Each push is a fresh subagent; a follow-up (rebuttal or reformat) continues the same subagent.

## Claude Code

Dispatch: one `Agent` call per push, all in one message, `subagent_type: "general-purpose"`, `prompt`: the brief. Keep each returned agent ID.

Follow-up (rebuttal or reformat): `SendMessage` with `to`: that agent ID, `message`: the follow-up text.

## Agent Zero

Dispatch: one `parallel` call with one `call_subordinate` per push. Use the default profile, `reset: true`, the brief as `message`, `target.md` as attachment:

~~~json
{
  "tool_name": "parallel",
  "tool_args": {
    "tool_calls": [
      {"tool_name": "call_subordinate", "tool_args": {"reset": true, "name": "elicit pre-mortem", "message": "<brief>", "attachments": ["/tmp/elicit/<slug>/target.md"]}},
      {"tool_name": "call_subordinate", "tool_args": {"reset": true, "name": "elicit assumption-audit", "message": "<brief>", "attachments": ["/tmp/elicit/<slug>/target.md"]}}
    ],
    "wait": true
  }
}
~~~

Keep each job's `context_id`.

Follow-up (rebuttal or reformat): `call_subordinate` with `reset: false`, `context_id`: that push's ID, `message`: the follow-up text. A new push always uses `reset: true`.

## Other CLI runtimes

Dispatch: run each brief as a fresh headless session in the shell, read-only, for example `codex exec --sandbox read-only "<brief>"` or `claude -p --permission-mode plan "<brief>"`. Save stdout as the push file.

Follow-up (rebuttal or reformat): a new headless session with the brief, then `Your earlier return:` and the push file, then the follow-up text.

## No subagents

Run at most two pushes yourself. Before each push, read `target.md` again; write the push in full and save it before you start the next one. Skip the rebuttal: REJECT takes only ground (a) or (b). Say in your final response that the pushes ran without cold readers.
