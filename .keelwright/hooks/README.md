# Keelwright hooks for Claude Code

Two hooks that make Keelwright rituals fire automatically instead of relying on the agent to remember. Source: [`settings.snippet.json`](settings.snippet.json).

> Hooks are executed by the Claude Code harness, not by the model. That's the point: a reminder the harness injects can't be "forgotten" the way an in-context instruction can.

---

## What each hook does

| Hook | Trigger | Effect | Ritual |
|---|---|---|---|
| **PostToolUse** (on `Bash`) | A `Bash` call whose command matches `git push`, `git merge`, an `--ff-only` merge, or `gh pr merge` | Prints a reminder to run the **state-change currency reconcile** — update the front-door docs (NEXT-STEPS cursor, ROADMAP) and any affected auto-memory. | 10 |
| **SessionEnd** | Session ends | Prints a **lessons-learned** reminder (append to `docs/lessons-learned/`, confirm cursor + memory current) **and** snapshots `MEMORY.md` into `.harness/memory-snapshots/` (best-effort, never fails the session; prunes to the newest 20). | 12 |

The PostToolUse hook only inspects the command string; it never runs git itself. The SessionEnd snapshot is a copy, guarded with `|| true` so a missing memory file can't break shutdown.

---

## Merge into `.claude/settings.json`

`settings.json` is a single JSON object, so you can't concatenate files — merge the `hooks` key.

**If you have no `.claude/settings.json` yet:** copy `settings.snippet.json` to `<repo>/.claude/settings.json` and delete the `"//"` comment keys (JSON has no comments; Claude Code tolerates `"//"` string keys, but cleaner to remove them).

**If you already have one:** merge the `hooks.PostToolUse` and `hooks.SessionEnd` arrays into your existing `hooks` object. Append to the arrays if they already exist — don't overwrite other hooks.

Quick merge with `jq` — **array-safe** (concatenates the hook arrays instead of replacing them):

```sh
jq -s '
  .[0] as $a | .[1] as $b
  | ($a * $b)                                   # deep-merge scalars/objects
  | .hooks.PostToolUse = (($a.hooks.PostToolUse // []) + ($b.hooks.PostToolUse // []))
  | .hooks.SessionEnd  = (($a.hooks.SessionEnd  // []) + ($b.hooks.SessionEnd  // []))
' .claude/settings.json adapters/claude-code/hooks/settings.snippet.json > .claude/settings.merged.json
# review the result, then:
mv .claude/settings.merged.json .claude/settings.json
```

> Why not plain `jq -s '.[0] * .[1]'`? `*` deep-merges objects but **replaces** arrays — it
> would silently drop any existing `PostToolUse`/`SessionEnd` hooks you already have. The
> recipe above explicitly concatenates those two arrays. Drop the `"//"` comment keys after merging.

---

## Environment variables used

The snippet uses portable, generic shell and these (optional) Claude Code env vars, each with a fallback:

| Var | Fallback | Used for |
|---|---|---|
| `CLAUDE_TOOL_INPUT` | — | The tool input inspected by PostToolUse (the git command). |
| `CLAUDE_PROJECT_DIR` | `.` | Where to write `.harness/memory-snapshots/`. |
| `CLAUDE_MEMORY_DIR` | `$HOME/.claude/memory` | Where `MEMORY.md` lives, for the snapshot. |

If your Claude Code version names these differently, adjust the `command` strings — the logic is intentionally simple (a `grep` guard + a guarded `cp`) so it's easy to port.

---

## Verify

1. Make a no-op commit and `git push` on a throwaway branch → you should see the ritual-10 reminder after the push.
2. End a session → you should see the ritual-12 reminder and a new file under `.harness/memory-snapshots/`.

If nothing prints, check that the hook `matcher` matches your tool name and that your shell has `grep`/`printf` (both POSIX-standard).

If the ritual-10 reminder never prints after a push (but the SessionEnd reminder works), your Claude Code version likely exposes the git command under a different env var than `CLAUDE_TOOL_INPUT` — the `grep` then matches an empty string and silently no-ops. To find the right name, temporarily prepend `env | grep -i '^CLAUDE_' >&2;` to the PostToolUse `command`, trigger a push, read which `CLAUDE_*` var holds the command, then point the matcher at it.
